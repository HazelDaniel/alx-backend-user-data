#!/usr/bin/env python3
"""
Main file
"""
from auth import Auth
import requests

EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"
BASE_URL = "http://127.0.0.1:5000"


def register_user(email: str, password: str) -> None:
    """this function should register users with the provided email and password"""
    pass


def log_in_wrong_password(email: str, password: str) -> None:
    """this attempts to login a user with an incorrect password"""
    pass


def profile_unlogged() -> None:
    """this attempts to access the user profile without loggin in"""
    pass


def log_in(email: str, password: str) -> str:
    """this authenticates the user to a login session and returns the session id"""
    return None


def profile_logged(session_id: str) -> None:
    """this attempts the profile endpoint with a valid session ID."""
    pass


def log_out(session_id: str) -> None:
    """this logs out the user with the provided session id"""
    pass


def reset_password_token(email: str) -> str:
    """this attempts to request a token for password reset"""
    return None


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """ this attempts to update the user password with the provided reset token and  new password"""
    pass


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
