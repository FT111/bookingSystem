from flask import session, redirect, url_for
from functools import wraps
import uuid
import os
import dotenv
import secrets


# Simple session authentication system - Not ideal for production
authToken = secrets.token_urlsafe(32)

dotenv.load_dotenv('../instance/.env')
appUsername = os.environ['APP_USERNAME']
appPassword = os.environ['APP_PASSWORD']

assert appUsername is not None, 'APP_USERNAME not found in .env'
assert appPassword is not None, 'APP_PASSWORD not found in .env'


def getSession() -> str:
    if 'uuid' not in session:
        session['uuid'] = uuid.uuid4()
    return str(session['uuid'])


def authenticateSession(username: str, password: str) -> bool:
    if username == appUsername and password == appPassword:
        session['token'] = authToken
        return True

    return False


def authCheck(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('token') != authToken:
            session['loginRedirect'] = url_for(f'pageRoutes.{func.__name__}')
            return redirect('/login')

        return func(*args, **kwargs)

    return wrapper


def apiAuthCheck(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('token') != authToken:
            return {'error': 'Not authenticated'}, 401

        return func(*args, **kwargs)

    return wrapper
