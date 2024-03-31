from flask import session
import uuid


def getSession() -> str:
    if 'uuid' not in session:
        session['uuid'] = uuid.uuid4()
    return str(session['uuid'])
