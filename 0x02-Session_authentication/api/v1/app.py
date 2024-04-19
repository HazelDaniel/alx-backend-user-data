#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


env_auth_type: str = os.environ.get("AUTH_TYPE")
auth = BasicAuth() if env_auth_type == "basic_auth" else Auth()
app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})


@app.before_request
def authentication():
    """Perform authentication before handling each request."""
    if auth:
        request.current_user = auth.current_user(request)
        print(f" the request path is {request.path}")
        if auth.require_auth(request.path, ['/api/v1/status/',
                                            '/api/v1/unauthorized/',
                                            '/api/v1/forbidden/',
                                            '/api/v1/auth_session/login/']):
            if not auth.authorization_header(request) \
                    and not auth.session_cookie(request):
                return abort(401)
            if not auth.current_user(request):
                return abort(403)
    return

@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    print("hitting the not found endpoint")
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized_error(error) -> str:
    """ Response handler for 401 unauthorized
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden_error(error) -> str:
    """ Response handler for 403 forbidden
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
