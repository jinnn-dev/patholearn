from app.crud.base import CRUDBase
from app.models.hint_image import HintImage
from app.schemas.hint_image import HintImageCreate, HintImageUpdate


class CrudHintImage(CRUDBase[HintImage, HintImageCreate, HintImageUpdate]):
    pass

crud_hint_image = CrudHintImage(HintImage)
