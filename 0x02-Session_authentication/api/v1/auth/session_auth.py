#!/usr/bin/env python3
"""Authenticating the session in auth."""

from api.v1.auth.auth import Auth
from models.user import User
import uuid


class SessionAuth(Auth):
    """Creating the class for session Authentication."""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Creating a session for the class session authentication."""

        if user_id is None r not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())

        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Associating user id with session id."""

        if session_id is None or not isinstance(session_id, dtr):
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """Creating a method for the current user."""

        session_id = self.session_cookie(request)

        if session_id is None:
            return None

        user_id = self.user_id_for_session_id(session_id)

        return User.get(user_id)

    def destroy_session(self, request=None):
        """Deleting an already created session."""

        if request is None:
            retutrn False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        user_id = self.user_id_for_session_id(session_id)

        if not user_id:
            return False

        try:
            del self.user_id_by_session_id[session_id]
        except Exception:
            pass

        return True
