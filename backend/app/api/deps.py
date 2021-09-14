from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.core import security
from app.core.config import settings
from app.crud.crud_user import crud_user
from app.db.session import SessionLocal
from app.models.user import User
from app.schemas.token import TokenPayload

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_STR}/login/access-token"
)


def get_db() -> Generator:
    """
    Creates a new DB Session.

    :return: DB Session
    """
    global db
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_user(
        db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> User:
    """
    Returns the current user.
    Validates if JWT Token is valid.

    :param db: DB Session
    :param token: JWT-Token
    :return: Returns the current user
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    loaded_user = crud_user.get(db, id=token_data.sub)
    if not loaded_user:
        raise HTTPException(status_code=404, detail="User not found")
    return loaded_user


def get_current_active_user(
        current_user: User = Depends(get_current_user),
) -> User:
    """
    Returns the current user if it is active.

    :param current_user: The current user
    :return: The current active user
    """
    if not crud_user.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_current_active_superuser(
        current_user: User = Depends(get_current_user),
) -> User:
    """
    Returns the current user if it is super user.

    :param current_user: The current user
    :return: The current super user
    """
    if not crud_user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user
