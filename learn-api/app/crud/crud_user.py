from typing import Any, Dict, Optional, Union, List

from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        """
        Returns the user to the given email

        :param db: DB-Session
        :param email: Email address of user
        :return: The found user
        """
        return db.query(self.model).filter(self.model.email == email).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        """
        Saves a new user.

        :param db: DB-Session
        :param obj_in: contains all relevant information for user creation
        :return: the created user
        """
        user = User()
        user.id = obj_in.id
        user.email = obj_in.email
        user.firstname = obj_in.firstname
        user.lastname = obj_in.lastname
        # user.hashed_password = get_password_hash(obj_in.password)
        user.is_superuser = obj_in.is_superuser
        user.last_login = obj_in.last_login
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def update(
        self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        """
        Updates the given user.

        :param db: DB-Session
        :param db_obj: user object loaded from DB
        :param obj_in: contains all data that should be updated
        :return: the updated user
        """
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if "password" in update_data and update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
        """
        Authenticates the user by the given email and password.

        :param db: DB-Session
        :param email: email of the user
        :param password: password of the user
        :return: user if valid credentials
        """
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def get_admin_users(self, db: Session) -> Optional[List[User]]:
        return db.query(self.model).filter(User.is_superuser == True).all()

    def is_active(self, user: User) -> bool:
        return user.is_active

    def is_superuser(self, user: User) -> bool:
        return user.is_superuser


crud_user = CRUDUser(User)
