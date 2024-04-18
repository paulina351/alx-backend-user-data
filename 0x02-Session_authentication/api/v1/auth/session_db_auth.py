#!/usr/bin/env python3
"""A task on session authentication"""

from api.v1.auth.session_exp_auth import SessionExpAuth
from datetime import datetime, timedelta
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """Create a new authentication class."""

    def create_session(self, user_id=None):
        """Creating a session that stores in user session."""
        session_id = super().create_session(user_id)

        if session_id is None:
            return None

        kwargs = {'user_id': user_id, 'session_id': session_id}
        user_session = UserSession(**kwargs)
        user_session.save()
        UserSession.save_to_file()

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Returns the user Id by requesting UserSession."""
        if session_id is None:
            return None

        UserSession.load_from_file()
        user_session = userSession.search({
            'session_id': session_id
        })

        if not user_session:
            return None

        user_session = user_session[0]

        expired_time = user_session.created_at + \
                timedelta(seconds=self.session_duration)

        if expired_time < datatime.utcnow():
            return None

        return user_session.user_id

    def destroy_session(self, request=None):
        """Destroys the UserSession based on the session ID."""
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        user_id = self.user_id_for_session_id(session_id)

        if not user_id:
            return False

        user_session = UserSession.search({
            session_id: session_id
        })

        if not user_session:
            return False

        user_session = user_session[0]

        try:
            user_session.remove()
            UserSession.save_to_file()
        except Exception:
            return False

        return True
