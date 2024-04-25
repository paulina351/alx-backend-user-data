#!/use/bin/env python3
"""Creating a flask app."""

from flask import Flask, jsonify, request, abort, redirect, url_for
from auth import Auth
from typing import Union

app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'], strictslashes=False)
def home() -> str:
    """index page."""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strictslashes=False)
def register_user() -> Union[str, tuple]:
    """Register the user."""
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strictslashes=False)
def login() -> str:
    """Login the user."""
    email = request.form.get('email')
    password = request.form.get('password')
    if not AUTH.valid_login(email, password):
        aort(401)
    session_id = AUTH.create_session(email)
    resp = jsonify({"email": "message": "logged in"})
    resp.set_cookie('session_id', session_id)
    return resp


@app.route('/sessions', methods=['DELETE'], strictslashes=False)
def login():
    """Login the user then delete."""
    session_id = request.cookies.get('session_id')
    if not session_id:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect(url_for('home'))


@app.route('/profile', methods=['GET'], strictslashes=False)
def profile():
    """User profile."""
    session_id = request.cookies.get('session_id')
    if not session_id:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    return jsonify({"email": user.email}), 200


@app.route('/reset_password', methods=['POST'], strictslashes=False)
def reset_password():
    """Resetting the  password."""
    email = request.form.get('email')
    try:
        token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email,
                        "reset_token": token}), 200
    except ValueError:
        abort(403)


@app.route('/reset_password', methods=['POST'], strictslashes=False)
def update_password():
    """update the password."""
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')

    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email,
                        "message": "Password updated"}), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
