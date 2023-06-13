from datetime import timedelta, datetime
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api import deps
from app.core import security
from app.core.config import settings
from app.crud.crud_user import crud_user
from app.models.user import User
from app.schemas.token import Token
from app.schemas.user import User as SchemaUser, UserUpdate

router = APIRouter()


@router.post("/login/access-token", response_model=Token)
def login_access_token(
    db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = crud_user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not crud_user.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")

    update_user = UserUpdate()
    update_user.last_login = datetime.now()
    crud_user.update(db, db_obj=user, obj_in=update_user)
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@router.post("/login", response_model=SchemaUser)
def login(db: Session = Depends(deps.get_db), form_data=User) -> Any:
    print(form_data.id)
    user = crud_user.get(db, id=form_data.id)
    if not user:
        raise HTTPException(status_code=400, detail="User could not be found")

    update_user = UserUpdate()
    update_user.last_login = datetime.now()
    updated_user = crud_user.update(db, db_obj=user, obj_in=update_user)
    return updated_user


@router.post("/login/test-token", response_model=SchemaUser)
def test_token(current_user: User = Depends(deps.get_current_user)) -> Any:
    """
    Test access token
    """
    return current_user
