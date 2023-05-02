import json
import requests

import app.schemas.user
from app.core.config import settings
from app.crud.crud_user import crud_user

# noinspection PyUnresolvedReferences
from app.db import base  # Import needed SQL Alchemy models
from app.db.base_class import Base
from app.db.session import engine
from app.core.security import get_password_hash
from sqlalchemy.orm import Session


def create_supertoken_user(email, password_hash):
    url = "http://supertokens:3567/recipe/user/passwordhash/import"
    body = {"email": email, "passwordHash": password_hash, "hashingAlgorithm": "bcrypt"}
    headers = {"content-type": "application/json"}

    result = requests.post(url, data=json.dumps(body), headers=headers)
    return result.json()["user"]["id"]


def set_metadata(user_id: str, firstname: str, lastname: str):
    url = "http://supertokens:3567/recipe/user/metadata"
    body = {
        "userId": user_id,
        "metadataUpdate": {"first_name": firstname, "last_name": lastname},
    }

    headers = {"content-type": "application/json"}

    result = requests.put(url, data=json.dumps(body), headers=headers)
    return result.status_code


def init_db(db: Session) -> None:
    """
    Creates initial database data.

    :param db: DB Session
    """
    Base.metadata.create_all(bind=engine)

    loaded_user = crud_user.get_by_email(db, email=settings.FIRST_SUPERUSER_EMAIL)
    if not loaded_user:
        user_id = create_supertoken_user(
            settings.FIRST_SUPERUSER_EMAIL,
            get_password_hash(settings.FIRST_SUPERUSER_PASSWORD),
        )
        set_metadata(
            user_id,
            settings.FIRST_SUPERUSER_FIRSTNAME,
            settings.FIRST_SUPERUSER_LASTNAME,
        )
        user_in = app.schemas.user.UserCreate(
            id=user_id,
            email=settings.FIRST_SUPERUSER_EMAIL,
            firstname=settings.FIRST_SUPERUSER_FIRSTNAME,
            lastname=settings.FIRST_SUPERUSER_LASTNAME,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        crud_user.create(db, obj_in=user_in)
