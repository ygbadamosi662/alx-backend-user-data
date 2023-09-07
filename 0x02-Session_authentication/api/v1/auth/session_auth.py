#!/usr/bin/env python3
""" File that create a Session Authentication Model
"""
from api.v1.auth.auth import Auth
from uuid import uuid4
from typing import TypeVar
from models.user import User


class SessionAuth(Auth):
    """
    Implementation of Session Authentication Model

    Args:
        Auth (TypeVar('Auth')): the authentication model
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        creates a Session ID for a user.

        Args:
            user_id (str, optional): current user id. Defaults to None.

        Returns:
            str: returns the session id
        """
        if not user_id or not isinstance(user_id, str):
            return None

        sess_id = str(uuid4())
        self.user_id_by_session_id[sess_id] = user_id
        return sess_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        returns a user id based on a session id

        Args:
            session_id (str, optional): the session id of the user.
            Defaults to None.

        Returns:
            str: the user id linked to the provided session id
        """
        if not session_id or not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> TypeVar('User'):
        """
        returns a User instance based on a cookie value.

        Args:
            request (str, optional): flask request object.

        Returns:
            TypeVar('User'): the user linked to the cookie value.
        """
        if not request:
            return None

        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)

        return User.get(user_id)

    def destroy_session(self, request=None):
        """
        deletes the user session / logout

        Args:
            request (_type_, optional): flask object reques.
            Defaults to None.
        """
        if not request:
            return False

        sess_id = self.session_cookie(request)
        if not sess_id:
            return False

        user_id = self.user_id_for_session_id(sess_id)
        if not user_id:
            return False

        del self.user_id_by_session_id[sess_id]
        return True
