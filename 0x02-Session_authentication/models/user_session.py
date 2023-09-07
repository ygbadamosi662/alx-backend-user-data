#!/usr/bin/env python3
""" A model that creates a session for the user
"""
from models.base import Base


class UserSession(Base):
    """
    Creates a new session for the user

    Args:
        Base (_type_): the base model inherited from
    """
    def __init__(self, *args: list, **kwargs: dict):
        if kwargs:
            for k, v in kwargs.items():
                setattr(self, k, v)
        else:
            self.user_id = args[0]
            self.session_id = args[1]
