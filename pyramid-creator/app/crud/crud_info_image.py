from app.crud.base import CRUDBase
from app.schemas.info_image import CreateInfoImage, InfoImage, UpdateInfoImage


class CRUDInfoImage(CRUDBase[InfoImage, CreateInfoImage, UpdateInfoImage]):
    pass


crud_info_image = CRUDInfoImage(InfoImage, "info_image_id")
