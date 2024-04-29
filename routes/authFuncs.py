from flask import session, redirect, url_for
from functools import wraps
import uuid
import os
import dotenv
import secrets
import hashlib


# Simple session authentication system - Not ideal for production
authToken = secrets.token_urlsafe(32)

# Loads environment variables from the .env file - Asserts that the required variables are present
dotenv.load_dotenv('../instance/.env')
appUsername = os.environ['APP_USERNAME']
appHash = os.environ['APP_AUTH_HASH']
appSalt = os.environ['APP_SALT']

assert appUsername is not None, 'APP_USERNAME not found in .env'
assert appHash is not None, 'APP_AUTH_HASH not found in .env'
assert appSalt is not None, 'APP_AUTH_SALT not found in .env'


# Generates a unique ID for each user session, stored in their cookie
def getSession() -> str:
    if 'uuid' not in session:
        session['uuid'] = uuid.uuid4()
    return str(session['uuid'])


def authenticateSession(username: str, password: str) -> bool:

    # Hashes the password with the salt and compares it to the stored hash
    password += appSalt
    passwordHash = hashlib.sha256(password.encode()).hexdigest()

    if username == appUsername and passwordHash == appHash:
        session['token'] = authToken
        return True

    return False


# Decorator to check if the user is authenticated - Redirects to the login page if not
def authCheck(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('token') != authToken:
            session['loginRedirect'] = url_for(f'pageRoutes.{func.__name__}', **kwargs)
            return redirect('/login')

        return func(*args, **kwargs)
    return wrapper


# Decorator for API routes to check if the user is authenticated - Returns an error if not
def apiAuthCheck(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('token') != authToken:
            return {'error': 'Not authenticated'}, 401

        return func(*args, **kwargs)
    return wrapper