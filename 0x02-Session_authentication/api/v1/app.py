#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os
from api.v1.auth.session_auth import SessionAuth
from api.v1.auth.session_exp_auth import SessionExpAuth


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None

if os.getenv("AUTH_TYPE") == 'auth':
    from api.v1.auth.auth import Auth
    auth = Auth()
if os.getenv("AUTH_TYPE") == 'basic_auth':
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()
if os.getenv("AUTH_TYPE") == 'session_auth':
    auth = SessionAuth()
if os.getenv('AUTH_TYPE') == 'session_exp_auth':
    from api.v1.auth.session_exp_auth import SessionExpAuth
    auth = SessionExpAuth()

@app.before_request
def request_filter() -> str:
    """
    Checks if the requested path requires authentication
    """
    excluded_paths = ['/api/v1/status/', '/api/v1/unauthorized/',
                      '/api/v1/forbidden/', '/api/v1/auth_session/login/']
    if auth is not None and auth.require_auth(request.path, excluded_paths):
        if (
            auth.authorization_header(request) is None
            and auth.session_cookie(request) is None
        ):
            return None, abort(401)
        current_user = auth.current_user(request)
        if current_user is None:
            abort(403)
        request.current_user = current_user


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized_user(error) -> str:
    """ Unauthorized user handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def no_access(error) -> str:
    """ No access handler"""
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
