from typing import List

from app.crud.base import CRUDBase
from app.schemas.slide import CreateSlide, Slide, SlideStatus, UpdateSlide
from pymongo.collection import Collection


class CRUDSlide(CRUDBase[Slide, CreateSlide, UpdateSlide]):
    def slide_with_name_exists(self, *, collection: Collection, name: str) -> bool:
        return collection.count_documents({"name": name}, limit=1) != 0

    def get_all_slides(
        self,
        *,
        collection: Collection,
        status: SlideStatus = None,
        with_metadata: bool = True
    ) -> List[Slide]:
        filter_query = {"_id": False, "metadata": with_metadata}
        where_query = {}
        if status != None:
            where_query["status"] = status
        return self.get_multi(
            collection, where_query=where_query, filter_query=filter_query
        )

    def get_all_slides_by_ids(
        self,
        *,
        collection: Collection,
        slide_ids: List[str],
        status: SlideStatus = None,
        with_metadata: bool = True
    ) -> List[Slide]:
        filter_query = {"_id": False, "metadata": with_metadata}
        where_query = {}
        if status != None:
            where_query["status"] = status
        return self.get_multi_by_ids(
            collection, slide_ids, where_query=where_query, filter_query=filter_query
        )

    def get_slide(
        self, *, collection: Collection, slide_id: str, with_metadata: bool = True
    ) -> Slide:
        return self.get(
            collection=collection,
            entity_id_value=slide_id,
            filter_qurey={"_id": False, "metadata": with_metadata},
        )


crud_slide = CRUDSlide(Slide, "slide_id")
