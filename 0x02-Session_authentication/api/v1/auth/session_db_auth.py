#!/usr/bin/env python3
"""module for the class SessionDBAuth"""

from api.v1.auth.session_exp_auth import SessionExpAuth
from datetime import datetime, timedelta
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """This class extends the capability of the SessionExpAuth class
        by persisting the sessions"""
    def create_session(self, user_id=None):
        """Creates a new session and saves it to a file"""
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        args = {"user_id": user_id, "session_id": session_id}
        user_session = UserSession(**args)
        user_session.save()
        user_session.save_to_file()

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """gets the user_id associated with the provided session_id"""
        if not session_id:
            return None

        UserSession.load_from_file()
        user_session = UserSession.search({'session_id': session_id})
        if not user_session:
            return None

        user_session = user_session[0]
        ex_time = user_session.created_at + timedelta(seconds=self.session_duration)
        if ex_time < datetime.utcnow():
            return None

        return user_session.user_id

    def destroy_session(self, request=None):
        """deletes the session tied to the given request"""
        if not request:
            return False
        session_id = self.session_cookie(request)
        if not session_id or not self.user_id_for_session_id(session_id):
            return False
        user_session = UserSession.search({"session_id": session_id})
        if not user_session:
            return False

        user_session[0].remove()
        UserSession.save_to_file()
        return True
