from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session

from app import models
from app.api import deps
from app.core.config import settings
from app.crud.crud_user import crud_user
from app.models.user import User
from app.schemas.user import User as UserSchema, UserCreate, UserUpdate

router = APIRouter()


@router.get("/", response_model=List[UserSchema])
def read_users(
    db: Session = Depends(deps.get_db),
    current_user: models.user.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Retrieve users.
    """
    users = crud_user.get_multi(db)
    return users


@router.get("/admin", response_model=List[UserSchema])
def read_admin_users(
    db: Session = Depends(deps.get_db),
    current_user: models.user.User = Depends(deps.get_current_active_superuser),
):
    return crud_user.get_admin_users(db)


@router.post("/admin", response_model=UserSchema)
def create_admin_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: UserCreate,
    current_user: models.user.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new user.
    """
    user = crud_user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user_in.is_superuser = True
    user = crud_user.create(db, obj_in=user_in)
    return user


@router.put("/me", response_model=UserSchema)
def update_user_me(
    *,
    db: Session = Depends(deps.get_db),
    password: str = Body(None),
    full_name: str = Body(None),
    email: EmailStr = Body(None),
    current_user: models.user.User = Depends(deps.get_current_user),
) -> Any:
    """
    Update own user.
    """
    current_user_data = jsonable_encoder(current_user)
    user_in = UserUpdate(**current_user_data)
    if password is not None:
        user_in.password = password
    if full_name is not None:
        user_in.full_name = full_name
    if email is not None:
        user_in.email = email
    user = crud_user.update(db, db_obj=current_user, obj_in=user_in)
    return user


@router.get("/me", response_model=UserSchema)
def read_user_me(
    db: Session = Depends(deps.get_db),
    current_user: models.user.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return current_user


@router.post("/open", response_model=UserSchema)
def create_user_open(*, db: Session = Depends(deps.get_db), user_in: UserCreate) -> Any:
    """
    Create new user without the need to be logged in.
    """
    if not settings.USERS_OPEN_REGISTRATION:
        raise HTTPException(
            status_code=403,
            detail="Open user registration is forbidden on this server",
        )
    user = crud_user.create(db, obj_in=user_in)
    return user


@router.get("/{user_id}", response_model=UserSchema)
def read_user_by_id(
    user_id: str,
    current_user: models.user.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific user by id.
    """
    user = crud_user.get(db, id=user_id)
    if user == current_user:
        return user
    if not crud_user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return user


@router.put("/{user_id}", response_model=UserSchema)
def update_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: str,
    user_in: UserUpdate,
    current_user: models.user.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update a user.
    """
    user = crud_user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system",
        )
    user = crud_user.update(db, db_obj=user, obj_in=user_in)
    return user
