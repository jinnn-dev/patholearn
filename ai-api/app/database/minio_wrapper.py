from typing import Any

from app.database.custom_minio_client import MinioClient
from PIL import Image


class MinioWrapper:
    dataset_bucket = "datasets"

    def __init__(self):
        self.minio_client = MinioClient()

    def init_buckets(self):
        self.minio_client.create_bucket(MinioWrapper.dataset_bucket)


minio_wrapper = MinioWrapper()
minio_wrapper.init_buckets()
