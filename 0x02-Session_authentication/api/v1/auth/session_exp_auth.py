#!/usr/bin/env python3
""" create a session expiration
"""
from os import getenv
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """
    This model create an expiration time for the session
    """
    def __init__(self):
        """ initialze the variable
        """
        self.session_duration = int(getenv('SESSION_DURATION', 0))

    def create_session(self, user_id=None) -> str:
        """
        create a session by calling create session from super and returning
        the session id.

        Args:
            user_id (_type_, optional): the user id. Defaults to None.

        Returns:
            str: the session id
        """
        sess_id = super().create_session(user_id)
        if not sess_id:
            return None

        self.user_id_by_session_id[sess_id] = {
            'user_id': user_id,
            'created_at': datetime.now()
        }

        return sess_id

    def user_id_for_session_id(self, session_id=None):
        """
        find and return the user_id from the session dictionary.

        Args:
            session_id (_type_, optional): _description_. Defaults to None.

        Returns:
            returns user_id
        """
        if not session_id or not isinstance(session_id, str):
            return None

        session_dict = self.user_id_by_session_id.get(session_id)
        if not session_dict or 'created_at' not in session_dict:
            return None

        if self.session_duration <= 0:
            return session_dict.get('user_id')

        created_time = session_dict.get('created_at')
        session_elapsed = timedelta(seconds=self.session_duration)

        if created_time + session_elapsed < datetime.now():
            return None

        return session_dict.get('user_id')
