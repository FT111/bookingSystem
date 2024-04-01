from flask import Flask
import secrets
from flask_cors import CORS

from routes.pageRoutes import pageRoutes
from routes.APIRoutes import apiRoutes

class BookingSystemWebApp():
    def __init__(self):
        self.app = Flask(__name__)
        CORS(self.app)

        # Used to sign cookies
        self.app.secret_key = secrets.token_urlsafe(16)

        self.app.register_blueprint(pageRoutes)
        self.app.register_blueprint(apiRoutes, url_prefix='/api')

    def run(self):
        # deepcode ignore RunWithDebugTrue: Development server
        self.app.run(debug=True, port=8000, host='0.0.0.0')


if __name__ == '__main__':
    webApp = BookingSystemWebApp()
    webApp.run()