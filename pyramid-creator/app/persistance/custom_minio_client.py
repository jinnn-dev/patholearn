import json
import os
from typing import Any

from minio import Minio
from minio.deleteobjects import DeleteObject


def policy(bucket_name):
    return {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "AWS": ["*"]
                },
                "Action": "s3:GetObject",
                "Resource": "arn:aws:s3:::" + bucket_name + "/*"
            }
        ]
    }


class MinioClient:

    def __init__(self):
        self.instance = Minio(
            endpoint=os.environ["MINIO_URL"] if "MINIO_URL" in os.environ else "minio:9000",
            access_key=os.environ["MINIO_ROOT_USER"],
            secret_key=os.environ["MINIO_ROOT_PASSWORD"],
            secure=False
        )

    def create_bucket(self, bucket_name: str) -> None:
        bucket = self.instance.bucket_exists(bucket_name)

        if not bucket:
            bucket = self.instance.make_bucket(bucket_name, 'eu')
            print("✔️ Bucket created")
            self.instance.set_bucket_policy(bucket_name, json.dumps(policy(bucket_name)))
            print("✔️ Bucket policy created")
        else:
            print("Bucket already exists")

    def create_object(self, *, bucket_name: str, file_name: str, file_content: Any, content_type: Any):
        try:
            self.instance.fput_object(bucket_name, file_name, file_content,
                                      metadata={'Content-type': content_type})
            print(f"✔️ {file_name} has been created")
        except Exception as exc:
            print(f"❌ {file_name} couldn't be created")
            print(exc)
            raise Exception(f"{file_name} could not be created")

    def delete_object(self, *, bucket_name: str, file_name: str):
        print(f"🚮 {file_name} has been deleted")
        self.instance.remove_object(bucket_name, file_name)

    def delete_folder(self, *, bucket_name: str, folder_path: str):
        delete_object_list = map(
            lambda x: DeleteObject(x.object_name),
            self.instance.list_objects(bucket_name, prefix=folder_path, recursive=True)
        )
        errors = self.instance.remove_objects(bucket_name, delete_object_list)

        for error in errors:
            print(error)

    def delete_all_objects(self, *, bucket_name: str):
        objects = self.instance.list_objects(bucket_name)
        for item in objects:
            self.instance.remove_object(bucket_name, item.object_name)
        print("✔️ All Objects deleted")

    def get_object(self, *, bucket_name: str, file_name: str):
        return self.instance.get_object(bucket_name, object_name=file_name)
