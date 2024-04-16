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
        """returns False - path and excluded_paths will be used
            later, now, you don’t need to take care of them
        """
        if path is None and excluded_paths is None or len(excluded_paths) == 0:
            return True
        path = path.rstrip('/') + '/'
        for pt in excluded_paths:
            pt = pt.rstrip('/') + '/'
            rp = re.escape(pt).replace('//*', '.*')
            if re.match(rp, path):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """returns None - request"""
        if request is None or 'Authorization' not in request.headers:
            return None
        return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        """returns None - request"""
        return None
