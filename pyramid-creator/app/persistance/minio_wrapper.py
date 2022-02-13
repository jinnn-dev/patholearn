from typing import Any

from app.persistance.custom_minio_client import MinioClient


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
        self.minio_client.delete_folder(bucket_name=MinioWrapper.pyramid_bucket, folder_path=slide_id)

    def create_task_image(self, *, file_name: str, file_content: Any, content_type: str = "image/jpeg"):
        self.minio_client.create_object(bucket_name=MinioWrapper.task_bucket,
                                        file_name=file_name,
                                        file_content=file_content,
                                        content_type=content_type)

    def delete_task_image(self, *, file_name: str):
        self.minio_client.delete_object(bucket_name=MinioWrapper.task_bucket, file_name=file_name)

    def create_info_image(self, *, file_name: str, file_content: Any, content_type: str = "image/jpeg"):
        self.minio_client.create_object(bucket_name=MinioWrapper.info_bucket,
                                        file_name=file_name,
                                        file_content=file_content,
                                        content_type=content_type)

    def delete_info_image(self, *, file_name: str):
        self.minio_client.delete_object(bucket_name=MinioWrapper.info_bucket, file_name=file_name)
