from flask import Flask
import os

import logging
logger = logging.getLogger(__name__)


def create_app(name=__name__):
    app = Flask(name)

    DIRECTORY = os.path.dirname(os.path.realpath(__file__))

    from torinotify import views

    app.register_blueprint(views.bp)

    return app


def run():
    app = create_app(name="torinotify")
    app.run(debug=True, port=5003, host="localhost")
