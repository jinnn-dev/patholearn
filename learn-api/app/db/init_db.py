import app.schemas.user
from app.core.config import settings
from app.crud.crud_user import crud_user

# noinspection PyUnresolvedReferences
from app.db import base  # Import needed SQL Alchemy models
from app.db.base_class import Base
from app.db.session import engine
from sqlalchemy.orm import Session


def init_db(db: Session) -> None:
    """
    Creates initial database data.

    :param db: DB Session
    """
    # Base.metadata.create_all(bind=engine)

    loaded_user = crud_user.get_by_email(db, email=settings.FIRST_SUPERUSER_EMAIL)
    if not loaded_user:
        user_in = app.schemas.user.UserCreate(
            email=settings.FIRST_SUPERUSER_EMAIL,
            firstname=settings.FIRST_SUPERUSER_FIRSTNAME,
            lastname=settings.FIRST_SUPERUSER_LASTNAME,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        crud_user.create(db, obj_in=user_in)
