import glob
import os
import shutil
from pprint import pprint

import pyvips
from celery import Celery
from celery.utils.log import get_task_logger

# from app.db.database import update_slide
from app.db.database import UpdateSlide, SlideStatus, slide_db
from app.persistance.custom_minio_client import MinioClient

celery_app = Celery(__name__)
celery_app.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "amqp://guest:guest@rabbit:5673//")

logger = get_task_logger(__name__)

OPENSLIDE_FORMATS = ["svs", "tif", "vms", "vmu", "ndpi", "scn", "mrxs", "tiff", "svslide", "bif"]

minio_client = MinioClient()
minio_client.create_bucket("pyramids")


@celery_app.task(name="convert_slide")
def convert_slide(file_name: str):
    """
       Converts WSI-Image to a image pyramid.

       :param file_name: Name of the WSI-Image
       :return: The convert status
       """
    file_id, file_extension = os.path.splitext(file_name)
    logger.info(file_name)
    pprint(vars(slide_db))

    try:
        # Save thumbnail
        can_openslide_load = file_extension in OPENSLIDE_FORMATS

        file_path = fr"./data/{file_id}/{file_name}"

        if can_openslide_load:
            try:
                thumbnail = pyvips.Image.openslideload(file_path, associated="thumbnail")
            except:
                image = pyvips.Image.openslideload(file_path)
                thumbnail = image.thumbnail_image(400)
            thumbnail.write_to_file(fr"./data/{file_id}/thumbnail.jpeg")
        else:
            image = pyvips.Image.new_from_file(file_path)
            thumbnail = image.thumbnail_image(400)
            thumbnail.write_to_file(fr"./data/{file_id}/thumbnail.jpeg")

        if can_openslide_load:
            image = pyvips.Image.openslideload(file_path)
        else:
            image = pyvips.Image.new_from_file(file_path)

        image.dzsave("dzi", dirname=fr"./data/{file_id}", tile_size=512)

        logger.info(image.get_fields())

        extracted_meta_data = {}

        for field in image.get_fields():
            extracted_meta_data[field] = image.get(field)

        files = [f for f in glob.glob(fr"./data/{file_id}/" + "**/*.jpeg", recursive=True)]

        for f in files:
            file = f.removeprefix("./data/")
            minio_client.create_object(str(file), f, "image/jpeg")
        minio_client.create_object(f"{file_id}/dzi.dzi", fr"./data/{file_id}/dzi.dzi", "text/xml")

        slide_db.update_slide(slide_id=file_id, slide_update=UpdateSlide(
            status=SlideStatus.SUCCESS,
            metadata=extracted_meta_data
        ))

        return {"status": "success"}
    except Exception as exc:
        # minio_client.delete_folder(f"{file_id}")
        slide_db.update_slide(slide_id=file_id, slide_update=UpdateSlide(
            status=SlideStatus.ERROR
        ))
        logger.error(exc)

        return {"status": "error"}
    finally:
        shutil.rmtree(fr"./data/{file_id}")
