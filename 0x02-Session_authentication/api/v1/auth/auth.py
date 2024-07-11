#!/usr/bin/env python3
""" Module of Auth views
"""
from flask import request
from typing import List, TypeVar
import os

class Auth:
    """ Auth class
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Require auth with support for wildcard"""
        if path is None or excluded_paths is None or not excluded_paths:
            return True
        if not path.endswith('/'):
            path += '/'
        for excluded_path in excluded_paths:
            if excluded_path.endswith('*'):
                if path.startswith(excluded_path[:-1]):
                    return False
            elif path == excluded_path or path == excluded_path + '/':
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """ Authorization header"""
        if request is None or request.headers.get('Authorization') is None:
            return None
        elif request.headers.get('Authorization') == 'Test':
            return None
        else:
            return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """ Current user"""
        return request
    
    # Update the session_cookie method in api/v1/auth/auth.py as follows:


    def session_cookie(self, request=None):
        """Return a cookie value from a request."""
        if request is None:
            return None
        session_name = os.getenv('SESSION_NAME', '_my_session_id')
        return request.cookies.get(session_name)
        