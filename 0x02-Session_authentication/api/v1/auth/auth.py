#!/usr/bin/env python3
""" file that setup authentication for users
"""
from flask import request
from typing import List, TypeVar
from os import getenv


class Auth:
    """
    Module that handles authentication for user using Basic Authentication
    system.
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        fetch the path and validate it
        Args:
            path (str): required path
            excluded_paths (List[str]): list of paths

        Returns:
            bool: True if valid or False if not
        """
        if not path or not excluded_paths:
            return True

        for i in excluded_paths:
            if i.endswith('*') and path.startswith(i[:-1]):
                return False
            elif i in {path, path + '/'}:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        check the header for authorization scheme and authorize the user
        based on the data.

        Args:
            request (Type, optional): Flask request object. Defaults to None.

        Returns:
            str: string
        """
        if not request or "Authorization" not in request.headers:
            return None

        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """
        returns the current user authenticated.

        Args:
            request ([type], optional): flask request object.
            Defaults to None.
        Returns:
            TypeVar('User'): the authenticated user object
        """
        return None

    def session_cookie(self, request=None) -> str:
        """
        get the cookie from the client browser.

        Args:
            request ([type], optional): flask request object.
            Defaults to None.
        Returns:

        """
        if not request:
            return None

        cookie_name = getenv('SESSION_NAME')
        if cookie_name:
            cookie = request.cookies.get(cookie_name)
            return cookie
        return None
