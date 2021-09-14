from typing import List, Optional

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.slide import Slide
from app.schemas.slide import SlideCreate, SlideUpdate


class CRUDSlide(CRUDBase[Slide, SlideCreate, SlideUpdate]):
    def get_all(self, db: Session) -> List[Slide]:
        """
        Returns all slides in DB.

        :param db: DB-Session
        :return: All available Slides
        """
        return db.query(self.model).all()

    def remove_by_file_id(self, db: Session, file_id: str):
        """
        Deletes the slide to the given file Id.

        :param db: DB-Session
        :param file_id: Id of the Slide
        :return: The deleted Slide
        """
        obj = db.query(self.model).filter(Slide.file_id == file_id).first()
        db.delete(obj)
        db.commit()
        return obj

    def update_slide(self, db: Session, obj_in: SlideUpdate) -> Slide:
        """
        Updates a slides.

        :param db: DB-Session
        :param obj_in: contains all information that should be updated
        :return:
        """
        db_obj = db.query(self.model).filter(Slide.file_id == obj_in.file_id).first()
        return self.update(db, db_obj=db_obj, obj_in=obj_in)

    def get_by_name(self, db: Session, *, name: str) -> Optional[Slide]:
        """
        Returns the Slides to the given name.

        :param db: DB-Session
        :param name: Name of the Slide
        :return: The found Slide
        """
        return db.query(self.model).filter(Slide.name == name).first()

    def get_by_file_id(self, db: Session, *, file_id: str) -> Slide:
        """
        Returns the Slide to the given file id
        :param db: DB-Session
        :param file_id: File ID of the slide
        :return: The found Slide
        """
        return db.query(self.model).filter(Slide.file_id == file_id).first()


crud_slide = CRUDSlide(Slide)
