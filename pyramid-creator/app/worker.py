import os
import shutil

from celery import Celery
from celery.utils.log import get_task_logger

from app.config import Config
from app.crud import crud_slide
from app.db.deps import get_slide_collection
from app.persistance.custom_minio_client import MinioClient
from app.persistance.minio_wrapper import MinioWrapper
from app.schemas.slide import SlideStatus, UpdateSlide
from app.utils.dicom import Dicom
from app.utils.slide_converter import SlideConverter

celery_app = Celery(__name__)
celery_app.conf.broker_url = os.environ.get(
    "CELERY_BROKER_URL", "amqp://guest:guest@rabbit:5673//")

logger = get_task_logger(__name__)

OPENSLIDE_FORMATS = ["svs", "tif", "vms", "vmu",
                     "ndpi", "scn", "mrxs", "tiff", "svslide", "bif"]

minio_client = MinioClient()
minio_client.create_bucket("pyramids")


@celery_app.task(name="convert_slide")
def convert_slide(source_file_with_extension: str):
    """
       Converts any image to a image pyramid.
       Image has to be stored on the disk beforehand.
       Otherwise, the conversion will not work.

       :param source_file: Name of the file
       :return: The convert status
       """
    slide_uuid, file_extension = os.path.splitext(source_file_with_extension)

    try:

        path_to_slide_folder = fr"{Config.TEMP_IMAGES_FOLDER}/{slide_uuid}"
        path_to_origin_file = fr"{Config.TEMP_IMAGES_FOLDER}/{slide_uuid}/{source_file_with_extension}"

        if file_extension.lower() == '.dcm':

            frame_uuids, metadata_dict = Dicom.save_dicom_frames(path_to_origin_file, slide_uuid)

            thumbnail_uuid = frame_uuids[len(frame_uuids) // 2]

            thumbnail_path = f"{path_to_slide_folder}/{thumbnail_uuid}/{thumbnail_uuid}.jpeg"

            SlideConverter.save_thumbnail(
                file_path=thumbnail_path,
                file_name_with_extension=source_file_with_extension,
                minio_client=minio_client,
            )

            for frame_uuid in frame_uuids:
                frame_path = f"{path_to_slide_folder}/{frame_uuid}/{frame_uuid}.jpeg"
                SlideConverter.save_deep_zoom(
                    file_path=frame_path,
                    dzi_folder_path=f"{path_to_slide_folder}/{frame_uuid}",
                    file_name_with_extension=source_file_with_extension,
                    minio_client=minio_client,
                    children=frame_uuids,
                    metadata=metadata_dict
                )
        else:
            SlideConverter.save_thumbnail(
                file_path=path_to_origin_file,
                file_name_with_extension=source_file_with_extension,
                minio_client=minio_client
            )

            SlideConverter.save_deep_zoom(
                file_path=path_to_origin_file,
                dzi_folder_path=path_to_slide_folder,
                file_name_with_extension=source_file_with_extension,
                minio_client=minio_client
            )

        return {"status": "success"}
    except Exception as exc:
        minio_client.delete_folder(bucket_name=MinioWrapper.pyramid_bucket, folder_path=f"{slide_uuid}")
        for connection in get_slide_collection():
            crud_slide.crud_slide.update(connection, entity_id_value=slide_uuid, obj_in=UpdateSlide(
                status=SlideStatus.ERROR
            ))

        logger.error(exc)
        return {"status": "error"}
    finally:
        shutil.rmtree(fr"{Config.TEMP_IMAGES_FOLDER}/{slide_uuid}")
