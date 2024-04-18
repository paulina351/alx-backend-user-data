#!/usr/bin/env python3
"""Create a class to manage the API authentication.
"""

from flask import request
from typing import List, TypeVar
import re


class Auth:
    """
        To create a class to manage the API authentication.
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """A public require authentication method that
            returns false to paths and excluded path.
        """
        if path is None and excluded_paths is None or \
            len(excluded_paths) == 0 \
                or (path not in excluded_paths and
                    "{}/".format(path) not in excluded_paths):
            return True
        return False

    def authorization_header(self, request=None) -> str:
        """returns None - request"""
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """returns None - request"""
        return None
