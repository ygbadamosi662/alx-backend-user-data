#!/usr/bin/env python3
"""
    this file consist of an SQLAlchemy model named User
    for a database table named users
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, VARCHAR, Column

Base = declarative_base()


class User(Base):
    """
    an SQLAlchemy model named User for a database table named users

    Args:
        Base (SQLAlchemy): sqlalchemy declarative base
    """
    __tablename__: str = "users"
    id = Column(Integer, primary_key=True)
    email = Column(VARCHAR(250), nullable=False)
    hashed_password = Column(VARCHAR(250), nullable=False)
    session_id = Column(VARCHAR(250))
    reset_token = Column(VARCHAR(250))
