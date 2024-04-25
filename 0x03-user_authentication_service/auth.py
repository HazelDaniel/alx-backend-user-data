#!/usr/bin/env python3
"""a module that provides an api for authentication"""

import bcrypt
import uuid
from db import DB
from user import User
from typing import Union
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """return a salted hash of the provided password string"""
    return bcrypt.hashpw(password.encode("utf8"), bcrypt.gensalt())


def _generate_uuid() -> str:
    """returns a string representation of a new UUID4"""
    return str(uuid.uuid4())


class Auth:
    """Authentication class -  a DAO authentication database."""
    def __init__(self):
        """Initialize a new instance of DB"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user with the provided email and password."""
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            user = self._db.add_user(email, _hash_password(password))
        else:
            raise ValueError(f"User {email} already exists")
        return user

    def valid_login(self, email: str, password: str) -> bool:
        """performs validation on user login credentials"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        return bcrypt.checkpw(password.encode("utf-8"), user.hashed_password)

    def create_session(self, email: str) -> str:
        """this method creates a user session with a provided email"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """this method gets a user to whom the provided session id is assigned"""
        if not session_id:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user

    def destroy_session(self, user_id: str):
        """this method deletes user session based on the provided user ID"""
        if user_id:
            self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """this generates a token for users that want to reset passwords"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError()
        reset_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str):
        """this method updates the user's password in the DB"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError()
        self._db.update_user(user.id,
                             hashed_password=_hash_password(password),
                             reset_token=None)
