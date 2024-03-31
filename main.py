from flask import Flask, render_template, request, redirect, url_for, Response, session, blueprints
from flask_cors import CORS
import json
import uuid
import os
import secrets

from routes.pageRoutes import pageRoutes
from routes.APIRoutes import apiRoutes


app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(16)
CORS(app)

app.register_blueprint(pageRoutes)
app.register_blueprint(apiRoutes)


if __name__ == '__main__':
    # deepcode ignore RunWithDebugTrue: Development server
    app.run(debug=True, port=8000, host='0.0.0.0')