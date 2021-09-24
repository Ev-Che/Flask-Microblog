"""The HTTP Basic Authentication, in which the client sends
the user credentials in a standard Authorization HTTP Header.
To integrate with Flask-HTTPAuth, the application needs to
provide two functions: one that defines the logic to check
the username and password provided by the user, and another
that returns the error response in the case of an authentication
failure.

The authenticated user will then be available as
basic_auth.current_user()"""
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth

from app.api.errors import error_response
from app.services import get_user_by_username, check_user_token

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()


@basic_auth.verify_password
def verify_password(username, password):
    user = get_user_by_username(username=username)
    if user and user.check_password(password=password):
        return user


@basic_auth.error_handler
def error_handler(status):
    return error_response(status)


@token_auth.verify_token
def verify_token(token):
    return check_user_token(token)


@token_auth.error_handler
def token_auth_error(status):
    return error_response(status)
