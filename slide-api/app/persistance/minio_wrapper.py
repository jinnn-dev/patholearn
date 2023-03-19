from typing import Any

from app.persistance.custom_minio_client import MinioClient
from PIL import Image
import io
import os
from pathlib import Path
import numpy as np
from cv2 import cv2
from loguru import logger


class MinioWrapper:
    hint_bucket = "hint-images"
    task_bucket = "task-images"
    info_bucket = "info-images"
    pyramid_bucket = "pyramids"

    def __init__(self):
        self.minio_client = MinioClient()

    def init_buckets(self):
        self.minio_client.create_bucket(MinioWrapper.hint_bucket)
        self.minio_client.create_bucket(MinioWrapper.task_bucket)
        self.minio_client.create_bucket(MinioWrapper.pyramid_bucket)
        self.minio_client.create_bucket(MinioWrapper.info_bucket)

    def delete_slide(self, slide_id: str):
        self.minio_client.delete_folder(
            bucket_name=MinioWrapper.pyramid_bucket, folder_path=slide_id
        )

    def create_task_image(
        self, *, file_name: str, file_content: Any, content_type: str = "image/jpeg"
    ):
        self.minio_client.create_object(
            bucket_name=MinioWrapper.task_bucket,
            file_name=file_name,
            file_content=file_content,
            content_type=content_type,
        )

    def delete_task_image(self, *, file_name: str):
        self.minio_client.delete_object(
            bucket_name=MinioWrapper.task_bucket, file_name=file_name
        )

    def create_info_image(
        self, *, file_name: str, file_content: Any, content_type: str = "image/jpeg"
    ):
        self.minio_client.create_object(
            bucket_name=MinioWrapper.info_bucket,
            file_name=file_name,
            file_content=file_content,
            content_type=content_type,
        )

    def delete_info_image(self, *, file_name: str):
        self.minio_client.delete_object(
            bucket_name=MinioWrapper.info_bucket, file_name=file_name
        )

    def get_slide_layers(self, slide_id: str):
        result = self.minio_client.get_object_names_in_folder(
            bucket_name=MinioWrapper.pyramid_bucket,
            parent_folder_path=f"{slide_id}/dzi_files/",
        )
        return list(result)

    def get_slide(self, slide_id: str, layer=0):

        object_path = f"{slide_id}/{layer}.jpeg"

        slide = self.minio_client.get_object(
            bucket_name=MinioWrapper.pyramid_bucket, object_path=object_path
        )

        if slide is not None:
            logger.info("Slide is cached")
            return slide
        logger.info("Slide is not cached")
        result = self.minio_client.get_objects_in_folder(
            bucket_name=MinioWrapper.pyramid_bucket,
            folder_path=f"{slide_id}/dzi_files/{layer}",
        )

        data = {}

        max_width = 0
        max_height = 0
        max_x = -1
        max_y = -1

        for image in result:
            base_name = Path(image["name"]).stem
            parsed_image = np.fromstring(image["data"], np.uint8)
            parsed_image = cv2.imdecode(parsed_image, cv2.COLOR_BGR2RGB)
            splitted = base_name.split("_")
            x = int(splitted[0])
            y = int(splitted[1])
            height = parsed_image.shape[0]
            width = parsed_image.shape[1]
            if x == 0:
                max_height += height
            if y == 0:
                max_width += width
            if x > max_x:
                max_x = x
            if y > max_y:
                max_y = y
            data[base_name] = parsed_image

        output_image = np.zeros(
            (max_height - max_y + 1, max_width - max_x + 1, 3), dtype=np.uint8
        )
        curr_x = 0
        for x in range(max_x + 1):
            update_x = 0
            curr_y = 0
            for y in range(max_y + 1):
                image = data[f"{str(x)}_{str(y)}"]
                height = image.shape[0]
                width = image.shape[1]

                output_image[
                    curr_y : curr_y + height,
                    curr_x : curr_x + width,
                ] = image

                curr_y += height - 1
                update_x = width - (1 if x > 0 else 0)

            curr_x += update_x
        _, im_jpg = cv2.imencode(".jpg", output_image)

        file_name = f"{layer}.jpeg"
        cv2.imwrite(file_name, output_image)

        self.minio_client.create_object(
            bucket_name=MinioWrapper.pyramid_bucket,
            file_name=f"{slide_id}/{file_name}",
            file_content=file_name,
            content_type="image/jpeg",
        )

        os.remove(file_name)

        return im_jpg.tobytes()
