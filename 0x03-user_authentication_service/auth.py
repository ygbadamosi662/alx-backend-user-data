#!/usr/bin/env python3
"""
    encrypt using bcrypt
"""
from bcrypt import hashpw, checkpw, gensalt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from typing import Union as U
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    """
    hash a password using bcrypt

    Args:
        password (str): password to hash
    """
    return hashpw(password.encode('utf-8'), gensalt())


def _generate_uuid() -> str:
    """
    generates a unique UUID
    """
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """
    def __init__(self):
        """ Initialize variables
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        register a new user

        Args:
            email (str): user email
            password (str): user password

        Returns:
            User: the new user object
        """
        try:
            obj = self._db.find_user_by(email=email)
            if obj:
                raise ValueError("User {} already exists".format(email))
        except NoResultFound:
            pass

        hashed_password: bytes = _hash_password(password)
        return self._db.add_user(email, hashed_password)

    def valid_login(self, email: str, password: str) -> bool:
        """
        valid user credentials for authorization

        Args:
            email (str): user email
            password (str): user password

        Returns:
            bool: true or false
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                if checkpw(password.encode('utf-8'), user.hashed_password):
                    return True
                return False

        except Exception:
            return False

    def create_session(self, email: str) -> str:
        """
        use the email param to generate a session id

        Args:
            email (str): user email

        Returns:
            str: the session id as string
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                sess_id = _generate_uuid()
                self._db.update_user(user.id, session_id=sess_id)

        except Exception:
            return None

        return sess_id

    def get_user_from_session_id(self, session_id: str) -> U[User, None]:
        """
        get the user from the provided session id

        Args:
            session_id (str): string

        Returns:
            User: current user object
        """
        if not session_id:
            return None

        try:
            return self._db.find_user_by(session_id=session_id)
        except Exception:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        Destroys the user session

        Args:
            user_id (int): user id
        """
        try:
            user = self._db.find_user_by(id=user_id)
            if user:
                self._db.update_user(user.id, session_id=None)
        except Exception:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """
        Generates a reset password token for the given email address

        Args:
            email (str): user email

        Returns:
            str: returns the token
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                reset = _generate_uuid()
                self._db.update_user(user.id, reset_token=reset)
                return reset

        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Updates the password of the user

        Args:
            reset_token (str): the token to reset
            password (str): the user new password
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            if user:
                hashed = _hash_password(password)
                new = {"hashed_password": hashed, "reset_token": None}
                self._db.update_user(user.id, **new)

        except NoResultFound:
            raise ValueError
