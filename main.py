from flask import Flask
import secrets
from flask_cors import CORS

from routes.pageRoutes import pageRoutes
from routes.APIRoutes import apiRoutes


app = Flask(__name__)
CORS(app)

# Used to sign cookies
app.secret_key = secrets.token_urlsafe(16)


app.register_blueprint(pageRoutes)
app.register_blueprint(apiRoutes, url_prefix='/api')


if __name__ == '__main__':
    # deepcode ignore RunWithDebugTrue: Development server
    app.run(debug=True, port=8000, host='0.0.0.0')