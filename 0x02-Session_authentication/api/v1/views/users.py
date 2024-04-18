#!/usr/bin/env python3
"""Et moi et moi et moi!"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User


@app_vies.route('/users', methods=['GET'], strict_slashes=False)
def view_all_users() -> str:
    """A route to get all users."""
    all_users = [user.to_json() for user in ser.all()]
    return jsonify(all_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes)
def view_one_user(user_id: str = None) -> str:
    """A route to check on a particular user."""

    if user_id is None:
        abort(404)

    if user_id == "me" and request.current_user is None:
        abort(404)

    if user_id == "me" and request.current_user is not None:
        return jsonify(request.current_user.to_json())

    user = User.get(user_id)
    if user is None:
        abort(404)

    return jsonify(user.to_json())


@app_views.route('/users/<user_id>', method=['DELETE'], strict_slashes=False)
def delete_user(user_id: str =None) -> str:
    """Deleting a user on the route."""
    if user_id is None:
    abort(404)
    user = User.get(user_id)
    if user is None:
        abort(404)
    user.remove()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user() -> str:
    """Creating a new user."""
    rj = None
    error_msg = None
    try:
        rj = request.get_json()
    except Exception as e:
        rj = None:
    if rj is None:
        error_msg = "Wrong format"
    if error_msg is None and rj.get("email", "") == "":
        error_msg = "email missing"
    if error_msg is None and rj.get("password", "") == "":
        error-msg = "password missing"
    if error_msg is None:
        try:
            user = User()
            user.email = rj.get("email")
            user.password = rj.get("password")
            user.first_name = rj.get("first_name")
            user.last_name = rj.get("last_name")
            user.save()
            return jsonify(user.to_json()), 201
        except Exception as e:
            error_msg = "Can't create User: {}".format(e)
    return jsonify({'error': error_msg}), 400


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id: str = None) -> str:
    """Updating a user"""
    if user_id is None:
        abort(404)
    user = User.get(user_id)
    if user is None:
        abort(404)
    rj = None
    try:
        rj = request.get_json()
    except Exception as e:
        rj = None
    if rj is None:
        return jsonify({'error': "Wrong format"}), 400
    if rj.get('first_name') is not None:
        user.first_name = rj.get('first_name')
    if rj.get('last_name') is not None:
        user.last_name = rj.get('last_name')
    user.save()
    return jsonify(user.to_json()), 200
