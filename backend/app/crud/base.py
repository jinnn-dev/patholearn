from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import flag_modified

from app.db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        :param model: A SQLAlchemy model class
        :param schema: A Pydantic model (schema) class
        """

        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        """
        General method to get an Entity by Id.

        :param db: DB-Session
        :param id: The id of the model
        :return: The found Entity or None
        """
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(self, db: Session) -> List[ModelType]:
        """
        Returns all Entities in DB.

        :param db: DB-Session
        :return: All found Entities
        """
        return db.query(self.model).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        """
        Creates a new Entity.

        :param db: DB-Session
        :param obj_in: Object containing all properties for creating the new entity
        :return: The created entity
        """
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
            self,
            db: Session,
            *,
            db_obj: ModelType,
            obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        """
        Updates the given entity.

        :param db: DB-Session
        :param db_obj: The entity to be updated
        :param obj_in: Object containing the properties that should be updated
        :return: The updated entity
        """
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
                flag_modified(db_obj, field)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, model_id: int) -> ModelType:
        """
        Removes the entity by the given id.

        :param db: DB-Session
        :param model_id: Id of the entity that should be deleted
        :return: The deleted entity
        """
        obj = db.query(self.model).get(model_id)
        db.delete(obj)
        db.commit()
        return obj
