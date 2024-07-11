#!/usr/bin/env python3
""" Module of Index views
"""
from api.v1.auth.auth import Auth
from uuid import uuid4
from models.user import User
from typing import Union, TypeVar
from flask import jsonify, request
from api.v1.views import app_views
import os


class SessionAuth(Auth):
    """ SessionAuth class
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ Create session """
        if user_id is None or type(user_id) is not str:
            return None
        session_id = uuid4()
        if session_id is None:
            return None
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ User id for session id """
        if session_id is None or type(session_id) is not str:
            return None
        return self.user_id_by_session_id.get(session_id)
    
    def current_user(self, request=None) -> Union[TypeVar('User'), None]:
        """
        Holds the current authenticated logged in user
        """
        User.load_from_file()
        return User.get(
            self.user_id_for_session_id(self.session_cookie(request))
        )
        
    
    @app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
    def session_login():
        """Handles all routes for the Session authentication."""
        email = request.form.get('email')
        if not email:
            return jsonify({"error": "email missing"}), 400
        password = request.form.get('password')
        if not password:
            return jsonify({"error": "password missing"}), 400
        users = User.search({'email': email})
        if not users:
            return jsonify({"error": "no user found for this email"}), 404

        user = users[0]
        if not user.is_valid_password(password):
            return jsonify({"error": "wrong password"}), 401

        session_id = Auth.create_session(user.id)
        response = jsonify(user.to_json())
        response.set_cookie(os.getenv('SESSION_NAME'), session_id)
        return response