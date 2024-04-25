#!/usr/bin/env python3
"""End-to-end integration test"""
import requests


def register_user(email: str, password: str) -> None:
    """Create one function for each of the following tasks.
        Arguments:
            email: the user's email.
            password: the user's password
        Return: None
    """
    req = requests.post('http://127.0.0.1:5000/users',
                        data={'email': email, 'password': password})
    if req.status_code == 200:
        assert (req.json() == {"email": email, "message": "user created"})
    else:
        assert(req.status_code == 400)
        assert(req.json() == {"message": "email already registered"})


def log_in_wrong_password(email: str, password: str) -> None:
    """Create one function for each of the following tasks.
        Arguments:
            email: the user's email.
            password: the user's password
        Return: None
    """
    req = requests.post('http://127.0.0.1:5000/sessions',
                        data={'email': email, 'password': password})
    assert (req.status_code == 401)


def log_in(email: str, password: str) -> str:
    """Create one function for each of the following tasks.

        Arguments:
            email: the user's email.
            password: the user's password
        Return: str
    """
    req = requests.post('http://127.0.0.1:5000/sessions',
                        data={'email': email, 'password': password})
    assert {req.status_code == 200}
    assert (req.json() == {"email": email, "message": "logged in"})
    return req.cookies['session_id']


def profile_unlogged() -> None:
    """Create one function for each of the following tasks.

        Arguments:
            Nil
        Return: None
    """
    req = requests.post('http://127.0.0.1:5000/profile')
    assert (req.status_code == 403)


def profile_logged(session_id: str) -> None:
    """Create one function for each of the following tasks.

        Arguments:
            session_id: the user's session id
        Return: None
    """
    cookies = {'session_id': session_id}
    req = requests.get('http://127.0.0.1:5000/profile',
                       cookies=cookies)
    assert(req.status_code == 200)


def log_out(session_id: str) -> None:
    """Create one function for each of the following tasks.
        Arguments:
            session_id: the user's session id
        Return: None
    """
    cookies = {'session_id': session_id}
    req = requests.delete('http://127.0.0.1:5000/sessions',
                          cookies=cookies)
    if req.status_code == 302:
        assert(req.url == 'http://127.0.0.1:5000/')
    else:
        assert(req.status_code == 200)


def reset_password_token(email: str) -> str:
    """Create one function for each of the following tasks.

        Arguments:
            email: the user's email.
        Return: str
    """
    req = requests.post('http://127.0.0.1:5000/reset_password',
                        data={'email': email})
    if req.status_code == 200:
        return req.json()["reset_token"]
    assert(req.status_code == 401)


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Create one function for each of the following tasks.

        Arguments:
            email: the user's email.
            reset_token: the user's token
            new_password: the user's password
        Return: None
    """
    data = {'email': email, 'reset_token': reset_token,
            'new_password': new_password}
    req = requests.put('http://127.0.0.1:5000/reset_password',
                       data=data)
    if req.status_code == 200:
        assert(req.json() == {"email": email, "message": "password updated"})
    else:
        assert(r.status_code == 403)


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


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
