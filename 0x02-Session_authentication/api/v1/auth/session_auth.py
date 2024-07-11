#!/usr/bin/env python3
""" Module of Index views
"""
from api.v1.auth.auth import Auth
from uuid import uuid4


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
    
    def current_user(self, request=None):
        """ Current user """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        return user_id