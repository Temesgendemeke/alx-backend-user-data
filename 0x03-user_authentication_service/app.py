#!/usr/bin/env python3
"""Auth module
"""
from flask import Flask, jsonify, request, abort,  redirect
from auth import Auth
import logging

logging.disable(logging.WARNING)
app = Flask(__name__)
auth = Auth()


@app.route("/", methods=["GET"], strict_slashes=False)
def basic_route():
    """ basic route """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=["POST"], strict_slashes=False)
def users():
    """ user route"""
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user = auth.register_user(email, password)
        if user:
            return jsonify({"email": user.email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=['POST'], strict_slashes=False)
def login() -> str:
    """ login route """
    email = request.form.get('email')
    password = request.form.get('password')
    if auth.valid_login(email, password):
        session_id = auth.create_session(email)
        if session_id:
            response = jsonify({"email": email, "message": "logged in"})
            response.set_cookie("session_id", session_id)
            return response
    return abort(403)


@app.route("/sessions", methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """ logut session """
    session_id = request.cookies.get("session_id")
    user = auth.get_user_from_session_id(session_id)
    if user:
        auth.destroy_session(user.id)
        return redirect("/")
    else:
        abort(403)


@app.route("/profile", methods=['GET'], strict_slashes=False)
def profile() -> str:
    """ profile route"""
    session = request.cookies.get("session_id")
    user = auth.get_user_from_session_id(session)
    if user:
        return jsonify({"email": user.email}), 200
    return abort(403)


@app.route("/reset_password", methods=['POST'], strict_slashes=False)
def get_reset_password_token() -> str:
    """ reset password route"""
    email = request.form.get('email')
    try:
        token = auth.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": token}), 200
    except ValueError:
        return abort(403)


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password() -> str:
    """ update password """
    email = request.form.get('email')
    new_pasword = request.form.get('password')
    reset_token = request.form.get('reset_token')
    if auth.get_reset_password_token(email) == reset_token:
        auth.update_password(reset_token, new_pasword)
        return jsonify({"email": email, "message": "Password updated"}), 200
    else:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
