import json
import os
from typing import Any

from app.core.config import settings
from minio import Minio
from minio.deleteobjects import DeleteObject


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
    hint_bucket = "hint-images"
    task_bucket = "task-images"

    def __init__(self):

        self.instance = Minio(
            endpoint=settings.MINIO_URL,
            access_key=settings.MINIO_ROOT_USER,
            secret_key=settings.MINIO_ROOT_PASSWORD,
            secure=False,
        )
        self.bucket = None
        self.bucket_name = None

    def create_bucket(self, bucket_name: str) -> None:
        self.bucket = self.instance.bucket_exists(bucket_name)
        self.bucket_name = bucket_name
        if not self.bucket:
            self.bucket = self.instance.make_bucket(bucket_name, "eu")
            print("✔️ Bucket created")
            self.instance.set_bucket_policy(
                self.bucket_name, json.dumps(policy(self.bucket_name))
            )
            print("✔️ Bucket policy created")
        else:
            print("Bucket already exists")

    def create_object(self, file_name: str, file_content: Any, content_type: Any):
        try:

            print(file_name, self.bucket_name)
            self.instance.fput_object(
                self.bucket_name,
                file_name,
                file_content,
                metadata={"Content-type": content_type},
            )
            print(f"✔️ {file_name} has been created")
        except Exception as exc:
            print(f"❌ {file_name} couldn't be created")
            print(exc)
            raise Exception()

    def delete_object(self, file_name: str):
        self.instance.remove_object(self.bucket_name, file_name)
        print(f"❌ {file_name} has ben deleted")

    def delete_slide(self, slide_id: str):
        # self.instance.remove_object(self.bucket_name, slide_id + '/')

        self.delete_folder(slide_id)

    def delete_folder(self, folder_path: str):
        # objects_to_delete = self.instance.list_objects(self.bucket_name, prefix=folder_path, recursive=True)
        delete_object_list = map(
            lambda x: DeleteObject(x.object_name),
            self.instance.list_objects(
                self.bucket_name, prefix=folder_path, recursive=True
            ),
        )
        errors = self.instance.remove_objects(self.bucket_name, delete_object_list)

        for error in errors:
            print(error)
        # for obj in objects_to_delete:
        #     self.instance.remove_object(self.bucket_name, obj.object_name)

    def delete_all_objects(self):
        objects = self.instance.list_objects(self.bucket_name)
        for item in objects:
            self.instance.remove_object(self.bucket_name, item.object_name)
        print("✔️ All Objects deleted")

    def get_object(self, file_name: str):
        return self.instance.get_object(self.bucket_name, object_name=file_name)


minio_client = MinioClient()
