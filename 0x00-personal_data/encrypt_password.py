#!/usr/bin/env python3
"""Encrypting passwords"""

import bcrypt
import hashlib
import base64


def hash_password(password: str) -> bytes:
    """User passwords should NEVER be stored
        in plain text in a database.
    """
    hash_passwd = bcrypt.hashpw(password.encode("utf-8"),
                                bcrypt.gensalt())
    return hash_passwd


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Implement an is_valid function that expects 2
        arguments and returns a boolean.
    """
    return bcrypt.checkpw(hashlib.sha256(password.encode()).digest(),
                          hashed_password)
