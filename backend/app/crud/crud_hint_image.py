from app.crud.base import CRUDBase
from app.schemas.hint_image import HintImage, HintImageCreate, HintImageUpdate


class CrudHintImage(CRUDBase[HintImage, HintImageCreate, HintImageUpdate]):
    pass
