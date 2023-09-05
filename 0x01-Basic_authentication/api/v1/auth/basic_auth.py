#!/usr/bin/env python3
""" File that create a Basic Authentication Model
"""
from api.v1.auth.auth import Auth
from models.user import User
import re
import base64
from typing import TypeVar
from flask import abort


class BasicAuth(Auth):
    """
    Implementation of Basic Authentication Model

    Args:
        Auth (TypeVar('Auth')): the authentication model
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        base64 authorization header

        Args:
            authorization_header (str): the string that start with basic.

        Returns:
            str: the base64 string extracted
        """
        if not authorization_header or type(authorization_header) != str:
            return None

        fetched = re.search(r'Basic\s+(.*)', authorization_header)
        if fetched:
            return fetched.group(1)
        return None

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """
        decode base64 authorization header

        Args:
            base64_authorization_header (str): the encoded string

        Returns:
            str: the decoded string
        """
        encoded = base64_authorization_header
        if not encoded or type(encoded) != str:
            return None
        try:
            data: bytes = base64.b64decode(base64_authorization_header)
            decoded_data: str = data.decode('utf-8')
        except (base64.binascii.Error, UnicodeDecodeError):
            return None
        return decoded_data

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """
        return a tuple containing the username and password

        Args:
            decoded_base64_authorization_header (str): the decoded string.

        Returns:
            (str, str): (username, password)
        """
        decoded = decoded_base64_authorization_header
        if not decoded or type(decoded) != str or ":" not in decoded:
            return None, None
        data = re.sub(r':', ',', decoded, count=1)
        return tuple(data.split(","))

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """
        return the user object gotten from the provided params

        Args:
            user_email (str): user email
            user_pwd (str): user password

        Returns:
            TypeVar('User'): the user object
        """
        if not user_email or not user_pwd:
            return None

        if type(user_email) != str or type(user_pwd) != str:
            return None

        try:
            database = User.search()
            if len(database) == 0:
                return None

            for user in database:
                if user.email == user_email:
                    if user.is_valid_password(user_pwd):
                        return user
            return None
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Get the current user logged in

        Args:
            request (flask object): the recent request

        Returns:
            TypeVar('User'): the user logged in
        """
        header = self.authorization_header(request)
        if not header:
            return None

        base = self.extract_base64_authorization_header(header)
        if not base:
            return None

        decode_base = self.decode_base64_authorization_header(base)
        if not decode_base:
            return None

        extra_cred = self.extract_user_credentials(decode_base)
        if not extra_cred:
            return None

        user_obj = self.user_object_from_credentials(extra_cred[0],
                                                     extra_cred[1])
        if not user_obj:
            return None

        return user_obj
