from flask import Flask
import secrets

from routes.pageRoutes import pageRoutes
from routes.APIRoutes import apiRoutes


class BookingSystemWebApp:
    """
    Main class for the web application. Responsible for setting up the Flask app and registering the
    routes.
    """

    def __init__(self):
        # Creates the Flask app
        self.app = Flask(__name__)

        # Used to sign cookies
        self.app.secret_key = secrets.token_urlsafe(16)

        self.app.register_blueprint(pageRoutes)
        self.app.register_blueprint(apiRoutes, url_prefix='/api')

    def run(self):
        self.app.run(port=8000, host='0.0.0.0')


# Used in WSGI servers
def createApp():
    return BookingSystemWebApp().app


if __name__ == '__main__':
    webApp = BookingSystemWebApp()
    webApp.run()
