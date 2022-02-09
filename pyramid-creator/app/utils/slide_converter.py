import glob

import pyvips
from app.config import Config
from app.crud import crud_slide
from app.db.deps import get_slide_collection
from app.persistance.custom_minio_client import MinioClient
from app.persistance.minio_wrapper import MinioWrapper
from app.schemas.slide import SlideStatus, UpdateSlide
from app.utils.slide_utils import (get_file_name_and_file_extension,
                                   openslide_can_load)


class SlideConverter:

    @staticmethod
    def save_thumbnail(file_path: str, file_name_with_extension: str, minio_client: MinioClient):
        """
        Saves a thumbnail of the file given by the file_path in the minio bucket.

        :param file_path: Path to the file
        :param file_name_with_extension: Name of the file with its extension
        :param minio_client: Instance of a MinioClient
        """
        file_id, file_extension = get_file_name_and_file_extension(file_name_with_extension)

        if openslide_can_load(file_extension):
            try:
                thumbnail = pyvips.Image.openslideload(
                    file_path,
                    associated="thumbnail"
                )
            except:
                image = pyvips.Image.openslideload(file_path)
                thumbnail = image.thumbnail_image(400)
        else:
            image = pyvips.Image.new_from_file(file_path)
            thumbnail = image.thumbnail_image(400)

        thumbnail_path = fr"{Config.TEMP_IMAGES_FOLDER}/{file_id}/thumbnail.jpeg"

        thumbnail.write_to_file(thumbnail_path)

        minio_client.create_object(
            bucket_name=MinioWrapper.pyramid_bucket,
            file_name=f"{file_id}/thumbnail.jpeg",
            file_content=thumbnail_path,
            content_type="image/jpeg"
        )

    @staticmethod
    def save_deep_zoom(file_path: str, dzi_folder_path: str, file_name_with_extension: str, minio_client: MinioClient, children=None, metadata={}):
        """
        Creates a DeepZoom of the file given by the file path.
        Stores it in minio and updates the database entry.

        :param file_path: Path to the file
        :param dzi_folder_path: Path to the folder where the deep zoom files should be stored
        :param file_name_with_extension: Name of the file with its extension
        :param minio_client: Instance of a MinioClient
        :param children: All children of the given file
        :param metadata: metadata of the file
        """
        file_id, file_extension = get_file_name_and_file_extension(file_name_with_extension)

        if openslide_can_load(file_extension):
            image = pyvips.Image.openslideload(file_path)
        else:
            image = pyvips.Image.new_from_file(file_path)

        image.dzsave("dzi", dirname=dzi_folder_path)

        pyramid_images_to_save = [image_path for image_path in glob.glob(
            fr"{dzi_folder_path}/dzi_files/**/*.jpeg", recursive=True
        )]

        for image_path in pyramid_images_to_save:
            minio_file_name = image_path.removeprefix(Config.TEMP_IMAGES_FOLDER)
            minio_client.create_object(
                bucket_name=MinioWrapper.pyramid_bucket,
                file_name=minio_file_name,
                file_content=image_path,
                content_type="image/jpeg"
            )

        dzi_minio_name = dzi_folder_path.removeprefix(Config.TEMP_IMAGES_FOLDER)

        minio_client.create_object(
            bucket_name=MinioWrapper.pyramid_bucket,
            file_name=fr"{dzi_minio_name}/dzi.dzi",
            file_content=fr"{dzi_folder_path}/dzi.dzi",
            content_type="text/xml"
        )

        if not metadata:
            metadata = SlideConverter.extract_metadata(image)

        slide_update = UpdateSlide(
            status=SlideStatus.SUCCESS,
            metadata=metadata,
            children=children,
        )

        for connection in get_slide_collection():
            crud_slide.crud_slide.update(
                connection,
                entity_id_value=file_id,
                obj_in=slide_update,
            )

    @staticmethod
    def extract_metadata(image: pyvips.Image):
        extracted_metadata = {}

        for field in image.get_fields():
            extracted_metadata[field] = image.get(field)

        return extracted_metadata
