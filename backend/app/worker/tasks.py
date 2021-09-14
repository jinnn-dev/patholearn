import os
import time

import pyvips
from celery import Celery, current_task
from celery.utils.log import get_task_logger

from app.core.config import settings
from app.crud.crud_slide import crud_slide
from app.db.session import SessionLocal
from app.schemas.slide import SlideUpdate

celery_app = Celery('tasks', broker=settings.RABBIT_URL, include=["app.worker.tasks"])
celery_app.conf.update(task_track_started=True)
logger = get_task_logger(__name__)


def eval_handler(image, progress):
    # print('run time so far (secs) = {}'.format(progress.run))
    # print('estimated time of arrival (secs) = {}'.format(progress.eta))
    # print('total number of pels to process = {}'.format(progress.tpels))
    # print('number of pels processed so far = {}'.format(progress.npels))
    # print('percent complete = {}'.format(progress.percent))
    pass


def benchmark():
    files = ["CMU-1-Small-Region.svs",
             "Session1_Test1.svs",
             "JP2K-33003-1.svs",
             "CMU-1.svs",
             "JP2K-33003-2.svs",
             "CMU-2.svs",
             ]
    sizes = [256, 512, 1024]
    for file in files:
        slide_path = os.path.join(os.getcwd(), f"data/slide/{file}")
        os.mkdir(slide_path)
        image = pyvips.Image.openslideload(f"./data/{file}")
        with open('./data/log.txt', 'a') as log_file:
            log_file.write(file + ": \n")
        for size in sizes:
            slide_path = os.path.join(os.getcwd(), f"data/slide/{file}/{size}")
            os.mkdir(slide_path)
            start_time = time.time()
            image.dzsave("dzi.dz", dirname=f"./data/slide/{file}/{size}", tile_size=size)
            image.set_progress(True)
            image.signal_connect('eval', eval_handler)
            with open('./data/log.txt', 'a') as log_file:
                log_file.write("\t" + str(size) + ": " + str((time.time() - start_time)) + "s\n")


@celery_app.task(name="create_slide.task")
def upload_task(filename: str):
    """
    Converts WSI-Image to a image pyramid.

    :param filename: Name of the WSI-Image
    :return: The convert status
    """
    db = SessionLocal()
    current_task.update_state(state='PROGRESS',
                              meta={'process_percent': 0})
    file_id, file_extension = os.path.splitext(filename)
    try:
        # Create directory for deepzoom file and thumbnail
        slide_path = os.path.join(os.getcwd(), f"data/slide/{file_id}")
        os.mkdir(slide_path)

        # Save thumbnail
        try:
            thumbnail = pyvips.Image.openslideload(f"./data/{filename}", associated="thumbnail")
            thumbnail.write_to_file(f"./data/slide/{file_id}/thumbnail.jpeg")
        except:
            image = pyvips.Image.openslideload(f"./data/{filename}")
            thumbnail = image.thumbnail_image(400)
            thumbnail.write_to_file(f"./data/slide/{file_id}/thumbnail.jpeg")

        # Generate deepzoom
        image = pyvips.Image.openslideload(f"./data/{filename}")
        image.set_progress(True)
        image.signal_connect('eval', eval_handler)
        image.dzsave("dzi.dz", dirname=f"./data/slide/{file_id}", tile_size=512)

        update_slide = SlideUpdate(file_id=file_id)

        try:
            update_slide.mag = image.get('openslide.objective-power')
        except Exception:
            pass

        try:
            update_slide.width = image.get('openslide.level[0].width')
        except Exception:
            pass

        try:
            update_slide.height = image.get('openslide.level[0].height')
        except Exception:
            pass

        try:
            update_slide.mpp = image.get('openslide.mpp-x')
        except Exception:
            pass

        update_slide.status = 'S'
        crud_slide.update_slide(db=db, obj_in=update_slide)
        # db.close()

        return {"status": "Successful"}
    except Exception as exc:
        update_slide = SlideUpdate(file_id=file_id, status='E')
        crud_slide.update_slide(db=db, obj_in=update_slide)

        print(exc)
        return {"status": "error"}
