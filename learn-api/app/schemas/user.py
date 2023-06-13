import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


# Shared properties
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    is_superuser: bool = False


# Properties to receive via API on creation
class UserCreate(UserBase):
    id: str
    email: EmailStr
    firstname: str
    lastname: str
    is_superuser: Optional[bool]
    last_login: Optional[datetime.datetime]


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None
    last_login: Optional[datetime.datetime] = None


class UserInDBBase(UserBase):
    id: Optional[str] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    pass


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str
