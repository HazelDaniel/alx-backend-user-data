#!/usr/bin/env python3
"""A module that defines the user class"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class User(Base):
    """The class that models the user table"""

    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    hashed_password = Column(String(250), nullable=False)
    reset_token = Column(String(250), nullable=True)
