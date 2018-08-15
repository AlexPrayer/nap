from flask import Flask

from utils import Router


class Application:
    def __init__(self):
        app = Flask(__name__)
        self.create_application(app)

    def create_application(self, app):
        app = Router().apply_routes(app)
        self.launch(app)

    @staticmethod
    def launch(app):
        app.run()


if __name__ == '__main__':
    application = Application()
