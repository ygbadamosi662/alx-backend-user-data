#!/usr/bin/env python3
""" create a db session for authentication
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """
    Save the session in a storage file

    Args:
        SessionExpAuth (_type_): Inherited Model
    """
    def create_session(self, user_id=None) -> str:
        """
        creates and stores new instance of UserSession and returns
        the session id

        Args:
            user_id (_type_, optional): _description_. Defaults to None.

        Returns:
            str : session id
        """
        sess_id = super().create_session(user_id)
        if not sess_id or type(sess_id) != str:
            return None

        # create and save the session in a file
        user_sess = UserSession([user_id, sess_id])
        user_sess.save()

        return sess_id

    def user_id_for_session_id(self, session_id=None) -> str:
        """
        returns the user id by requesting UserSession in the database
        based on session_id

        Args:
            session_id (_type_, optional): the current session id.
            Defaults to None.

        Returns:
            str: user id
        """
        data = UserSession.get(session_id)
        if not data:
            return None
        return data.user_id

    def destroy_session(self, request=None):
        """
        destroys the UserSession based on the Session ID from the
        reques tcookie

        Args:
            request (_type_, optional): flask object. Defaults to None.
        """
        if not request:
            return None

        sess_id = self.session_cookie(request)
        if not sess_id:
            return False

        data = UserSession.get(sess_id)
        if not data:
            return None

        data.remove()
