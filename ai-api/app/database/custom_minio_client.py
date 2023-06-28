import json
import os
from typing import Any

from minio import Minio
from minio.deleteobjects import DeleteObject
from loguru import logger

logger.add("minio_client.log", retention="1 week")


def policy(bucket_name):
    return {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {"AWS": ["*"]},
                "Action": "s3:GetObject",
                "Resource": "arn:aws:s3:::" + bucket_name + "/*",
            }
        ],
    }


class MinioClient:
    def __init__(self):
        self.instance = Minio(
            endpoint=os.environ["MINIO_URL"]
            if "MINIO_URL" in os.environ
            else "minio:9000",
            access_key=os.environ["MINIO_ROOT_USER"],
            secret_key=os.environ["MINIO_ROOT_PASSWORD"],
            secure=os.environ.get("MINIO_SECURE", False),
        )

    def create_bucket(self, bucket_name: str) -> None:
        bucket = self.instance.bucket_exists(bucket_name)

        if not bucket:
            self.instance.make_bucket(bucket_name, "eu")
            logger.info("Bucket {} created", bucket_name)
            self.instance.set_bucket_policy(
                bucket_name, json.dumps(policy(bucket_name))
            )
            logger.info("Policy for Bucket {} created", bucket_name)
        else:
            logger.info("Bucket {} already exists", bucket_name)

    def create_object(
        self, *, bucket_name: str, file_name: str, file_content: Any, content_type: Any
    ):
        try:
            self.instance.fput_object(
                bucket_name,
                file_name,
                file_content,
                metadata={"Content-type": content_type},
            )
            logger.info("✔️ {} has been created", file_name)
        except Exception as exc:
            logger.error(
                "{file_name} couldn't be created: \n{err}", file_name=file_name, err=exc
            )
            raise Exception(f"{file_name} could not be created")

    def delete_object(self, *, bucket_name: str, file_name: str):
        logger.info("{} has been deleted", file_name)
        self.instance.remove_object(bucket_name, file_name)

    def delete_folder(self, *, bucket_name: str, folder_path: str):
        delete_object_list = map(
            lambda x: DeleteObject(x.object_name),
            self.instance.list_objects(bucket_name, prefix=folder_path, recursive=True),
        )

        errors = self.instance.remove_objects(bucket_name, delete_object_list)
        error_count = 0
        for error in errors:
            logger.error(error)
            error_count += 1
        if error_count == 0:
            logger.info("Deleted folder {}", folder_path)

    def delete_all_objects(self, *, bucket_name: str):
        objects = self.instance.list_objects(bucket_name)
        for item in objects:
            self.instance.remove_object(bucket_name, item.object_name)
        logger.info("✔️ All Objects deleted")

    def get_object_names_in_folder(self, *, bucket_name: str, parent_folder_path: str):
        return self.instance.list_objects(bucket_name, prefix=parent_folder_path)

    def get_object(self, *, bucket_name: str, object_path: str):
        try:
            result = self.instance.get_object(bucket_name, object_path)
            return result.data
        except:
            return None

    def get_objects_in_folder(self, *, bucket_name: str, folder_path: str):
        images = self.instance.list_objects(
            bucket_name, prefix=folder_path, recursive=True
        )
        result_images = []
        for image in images:
            try:
                # print(image.object_name)
                obj = self.instance.get_object(bucket_name, image.object_name)
                result_images.append({"name": image.object_name, "data": obj.data})
            finally:
                obj.close()
                obj.release_conn()
        return result_images
