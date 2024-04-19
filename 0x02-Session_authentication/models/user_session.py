#!/usr/bin/env python3
"""This module creates a class for the user session"""

from models.base import Base


class UserSession(Base):
    """This class implements the creation of
        user session and assignment of user session id"""

    def __init__(self, *args: list, **kwargs: dict):
        """instance initializer for the class"""
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get("user_id")
        self.session_id = kwargs.get("session_id")
