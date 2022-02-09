from typing import List

from app.crud.base import CRUDBase
from app.schemas.slide import CreateSlide, Slide, UpdateSlide
from pymongo.collection import Collection


class CRUDSlide(CRUDBase[Slide, CreateSlide, UpdateSlide]):

    def slide_with_name_exists(self, *, collection: Collection, name: str) -> bool:
        return collection.count_documents({'name': name}, limit=1) != 0

    def get_all_slides(self, *, collection: Collection, with_metadata: bool = True) -> List[Slide]:
        return self.get_multi(collection, {'_id': False, 'metadata': with_metadata})

    def get_all_slides_by_ids(self, *, collection: Collection, slide_ids: List[str], with_metadata: bool = True) -> \
            List[Slide]:
        return self.get_multi_by_ids(collection, slide_ids, {'_id': False, 'metadata': with_metadata})

    def get_slide(self, *, collection: Collection, slide_id: str, with_metadata: bool = True) -> Slide:
        return self.get(collection=collection, entity_id_value=slide_id, filter_qurey={'_id': False, 'metadata': with_metadata})


crud_slide = CRUDSlide(Slide, "slide_id")
