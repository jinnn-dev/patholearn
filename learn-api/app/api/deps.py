from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session
from starlette.background import BackgroundTasks

from app.core import security
from app.core.config import settings
from app.crud.crud_base_task import crud_base_task
from app.crud.crud_course import crud_course
from app.crud.crud_user import crud_user
from app.db.session import SessionLocal, SessionManager, close_session
from app.models.user import User
from app.schemas.token import TokenPayload
from supertokens_python.recipe.session.framework.fastapi import verify_session
from supertokens_python.recipe.session import SessionContainer

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_STR}/login/access-token"
)


# def get_db() -> Generator:
#     """
#     Creates a new DB Session.
#
#     :return: DB Session
#     """
#     global db
#     try:
#         db = SessionLocal()
#         yield db
#     finally:
#         db.close()


def get_db(background_tasks: BackgroundTasks):
    with SessionManager() as db:
        background_tasks.add_task(close_session, db)
        yield db


def get_current_user_back(
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


async def get_current_user(
    db: Session = Depends(get_db), s: SessionContainer = Depends(verify_session())
):
    user_id = s.get_user_id()
    loaded_user = crud_user.get(db, id=user_id)

    return loaded_user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    return current_user


def get_current_active_user_BACK(
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


def check_if_user_can_access_course(db: Session, user_id: str, course_id: int) -> None:
    if not crud_course.user_is_course_owner(db, user_id=user_id, course_id=course_id):
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )


def check_if_user_can_access_task(
    db: Session, *, user_id: str, base_task_id: int
) -> None:
    base_task = crud_base_task.get(db, id=base_task_id)
    check_if_user_can_access_course(db, user_id=user_id, course_id=base_task.course_id)
