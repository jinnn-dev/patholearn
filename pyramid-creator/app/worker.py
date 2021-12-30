import glob
import os
import shutil
import time

import numpy
import numpy as np
import pyvips
from celery import Celery
from celery.utils.log import get_task_logger

# from app.db.database import update_slide
from pydicom.data import get_testdata_file

from app.config import Config
from app.crud import crud_slide
from app.db.deps import get_slide_collection
from app.persistance.custom_minio_client import MinioClient
from app.persistance.minio_wrapper import MinioWrapper
from app.schemas.slide import SlideStatus, UpdateSlide
from pydicom import dcmread
import pydicom

import matplotlib.pyplot as plt
from PIL import Image

from app.utils.dicom import Dicom

celery_app = Celery(__name__)
celery_app.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "amqp://guest:guest@rabbit:5673//")

logger = get_task_logger(__name__)

OPENSLIDE_FORMATS = ["svs", "tif", "vms", "vmu", "ndpi", "scn", "mrxs", "tiff", "svslide", "bif"]

minio_client = MinioClient()
minio_client.create_bucket("pyramids")


@celery_app.task(name="convert_slide")
def convert_slide(file_name: str):
    """
       Converts any image to a image pyramid.
       Image has to be stored on the disk beforehand.
       Otherwise, the conversion will not work.

       :param file_name: Name of the file
       :return: The convert status
       """
    file_id, file_extension = os.path.splitext(file_name)

    logger.info(file_extension)

    try:
        # Save thumbnail
        can_openslide_load = file_extension in OPENSLIDE_FORMATS

        folder_path = fr"{Config.TEMP_IMAGES_FOLDER}/{file_id}"
        file_path = fr"{Config.TEMP_IMAGES_FOLDER}/{file_id}/{file_name}"

        if can_openslide_load:
            try:
                thumbnail = pyvips.Image.openslideload(file_path, associated="thumbnail")
            except:
                image = pyvips.Image.openslideload(file_path)
                thumbnail = image.thumbnail_image(400)
            thumbnail.write_to_file(fr"{Config.TEMP_IMAGES_FOLDER}/{file_id}/thumbnail.jpeg")
        elif file_extension.lower() == '.dcm':
            pass
        else:
            image = pyvips.Image.new_from_file(file_path)
            thumbnail = image.thumbnail_image(400)
            thumbnail.write_to_file(fr"./data/{file_id}/thumbnail.jpeg")

        if file_extension.lower() == '.dcm':

            # image = pyvips.Image.magickload(file_path)
            # logger.info(image)
            # path = get_testdata_file("CT_small.dcm")
            # path = get_testdata_file(file_path)
            frame_uuids = Dicom.save_dicom_frames(file_path, file_id)

            thumbnail_uuid = frame_uuids[len(frame_uuids) // 2]
            thumbnail = pyvips.Image.new_from_file(f"{folder_path}/{thumbnail_uuid}/{thumbnail_uuid}.jpeg")
            thumbnail_path = fr"{folder_path}/thumbnail.jpeg"
            thumbnail.write_to_file(thumbnail_path)
            minio_client.create_object(bucket_name=MinioWrapper.pyramid_bucket, file_name=f"{file_id}/thumbnail.jpeg",
                                       file_content=thumbnail_path,
                                       content_type="image/jpeg")

            for frame_uuid in frame_uuids:
                image = pyvips.Image.new_from_file(f"{folder_path}/{frame_uuid}/{frame_uuid}.jpeg")
                image.dzsave("dzi", dirname=fr"{folder_path}/{frame_uuid}")

            for frame_uuid in frame_uuids:
                logger.info(glob.glob(fr"{folder_path}/" + "**/*.jpeg", recursive=True))
                files = [f for f in glob.glob(fr"{folder_path}/{frame_uuid}/dzi_files" + "**/*.jpeg", recursive=True)]
                logger.info(files)
                for f in files:
                    file = f.removeprefix("./data")
                    minio_client.create_object(bucket_name=MinioWrapper.pyramid_bucket, file_name=str(file),
                                               file_content=f,
                                               content_type="image/jpeg")
                minio_client.create_object(bucket_name=MinioWrapper.pyramid_bucket,
                                           file_name=f"{file_id}/{frame_uuid}/dzi.dzi",
                                           file_content=fr"./data/{file_id}/{frame_uuid}/dzi.dzi",
                                           content_type="text/xml")

            first_element = frame_uuids.pop(0)
            logger.info(frame_uuids)
            for connection in get_slide_collection():
                crud_slide.crud_slide.update(connection, entity_id_value=first_element, obj_in=UpdateSlide(
                    status=SlideStatus.SUCCESS,
                    metadata={},
                    children=frame_uuids
                ))
        else:
            if can_openslide_load:
                image = pyvips.Image.openslideload(file_path)
            else:
                image = pyvips.Image.new_from_file(file_path)
            image.dzsave("dzi", dirname=fr"./data/{file_id}", tile_size=512)
            logger.info(image.get_fields())
            extracted_meta_data = {}

            for field in image.get_fields():
                extracted_meta_data[field] = image.get(field)

            logger.info(extracted_meta_data)

            files = [f for f in glob.glob(fr"./data/{file_id}/" + "**/*.jpeg", recursive=True)]

            for f in files:
                print(f)
                file = f.removeprefix("./data/")
                minio_client.create_object(bucket_name=MinioWrapper.pyramid_bucket, file_name=str(file), file_content=f,
                                           content_type="image/jpeg")
            minio_client.create_object(bucket_name=MinioWrapper.pyramid_bucket, file_name=f"{file_id}/dzi.dzi",
                                       file_content=fr"./data/{file_id}/dzi.dzi", content_type="text/xml")

            for connection in get_slide_collection():
                crud_slide.crud_slide.update(connection, entity_id_value=file_id, obj_in=UpdateSlide(
                    status=SlideStatus.SUCCESS,
                    metadata=extracted_meta_data
                ))
        return {"status": "success"}
    except Exception as exc:
        # minio_client.delete_folder(f"{file_id}")
        for connection in get_slide_collection():
            crud_slide.crud_slide.update(connection, entity_id_value=file_id, obj_in=UpdateSlide(
                status=SlideStatus.ERROR
            ))
        # crud_slide.update_slide(slide_id=file_id, slide_update=UpdateSlide(
        #     status=SlideStatus.ERROR
        # ))

        logger.error(exc)
        return {"status": "error"}
    finally:
        pass
        # shutil.rmtree(fr"./data/{file_id}")
