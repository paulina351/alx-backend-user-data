#!/usr/bin/env python3
"""Sessions in database
"""
from models.base import Base


class UserSession(Base):
    """Create a new model UserSession that inherits from base.
    """

    def __init__(self, *args: list, **kwargs: dict):
        """Initializing the class."""
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.gGet('user_id')
        self.session_id = kwargs.get('session_id')
