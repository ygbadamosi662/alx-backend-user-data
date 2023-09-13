#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from user import Base, User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError


class DB:
    """ DB class """

    def __init__(self) -> None:
        """ Initialize a new DB instance """
        self._engine = create_engine("sqlite:///a.db")
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """ Memoized session object """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        create user and add to the database

        Args:
            email (str): new user email
            hashed_password (str): new user password
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """
        find user by key-value pair and return the first result.

        Args:
            kwargs (Dict[str: str]): the key-value pair.
        """
        try:
            obj = self._session.query(User).filter_by(**kwargs).first()
        except TypeError:
            raise InvalidRequestError
        if not obj:
            raise NoResultFound
        return obj

    def update_user(self, user_id: int, **kwargs) -> None:
        """ Finds user record and updates attributes """
        user_found = self.find_user_by(id=user_id)

        for key, value in kwargs.items():
            if hasattr(user_found, key):
                setattr(user_found, key, value)
            else:
                raise ValueError

        self._session.commit()
        return None
