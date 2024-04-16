#!/usr/bin/env python3
"""Basic auth"""

import base64
import binascii
import re

from typing import Tuple, TypeVar
from .auth import Auth
from models.user import User


class BasicAuth(Auth):
    """Class BasicAuth that inherits from Auth.
        For the moment this class will be empty.

    """
    def extract_base64_authorization_header(
            self,
            authorization_header: str) -> str:
        """In the class BasicAuth that returns the Base64 part
            of the Authorization header for a Basic Authentication.
        """
        if type(authorization_header) == str:
            pattern = r'Basic (?P<token>.+)'
            basic_holb = re.fullmatch(pattern, authorization_header.strip())
            if basic_holb is not None:
                return basic_holb.group('token')
        return None

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str) -> str:
        """In the class BasicAuth that returns the decoded value of a
            Base64 string base64_authorization_header.
        """
        if type(base64_authorization_header) == str:
            try:
                res = base64.b64decode(
                    base64_authorization_header,
                    validate=True,
                )
                return res.decode('utf-8')
            except (binascii.Error, UnicodeDecodeError):
                return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str,
            ) -> Tuple[str, str]:
        """In the class BasicAuth that returns the user email
            and password from the Base64 decoded value.
        """
        if type(decode_base64_authorization_header) == str:
            pattern = r'(?P<user>[^:]+):(?P<password>.+)'
            basic_holb = re.fullmatch(
                pattern,
                decoded_base64_authorization_header.strip(),
            )
            if basic_holb is not None:
                user = basic_holb.group('user')
                password = basic_holb.group('password')
                return user, password
        return None, None

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str) -> TypeVar('User'):
        """ In the class BasicAuth that returns the User
            instance based on his email and password.
        """
        if type(user_email) == str and type(user_pwd) == str:
            try:
                users = User.search({'email': user_email})
            except Exception:
                return None
            if len(users) <= 0:
                return None
            if users[0].is_valid_password(user_pwd):
                return user[0]
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """In the class BasicAuth that overloads Auth and
            retrieves the User instance for a request.
        """
        auth_header = self.authorization_header(request)
        b64_auth_token = self.extract_base64_authorization_header(auth_header)
        auth_token = self.decode_base64_authorization_header(b64_auth_token)
        email, password = self.extract_user_credentials(auth_token)
        return self.user_object_from_credentials(email, password)
