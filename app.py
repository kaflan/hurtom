#!/usr/bin/env python3
import logging
from logging.handlers import RotatingFileHandler

from flask import Flask, request
from flask.ext.babelex import Babel
from flask.ext.gravatar import Gravatar

from config import LANGUAGES
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CsrfProtect


def make_app(name=__name__):
    """
    create your application in a function and register blueprints on it. That way you can create multiple instances
    of your application with different configurations attached which makes unittesting a lot easier.
    You can use this to pass in configuration as needed.
    """
    # return app
app = Flask(__name__)
app.config.from_object('config')
app.config.from_object('instance.config')
db = SQLAlchemy(app)
CsrfProtect(app)
babel = Babel(app)
gravatar = Gravatar(app,
                    size=100,
                    rating='g',
                    default='retro',
                    force_default=False,
                    force_lower=False,
                    use_ssl=False,
                    base_url=None)


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(LANGUAGES.keys())

if True:
    from login_views import *
    from views import *
    from models import Base


if __name__ == '__main__':
    print(app.url_map)
    print(app.instance_path)
    print(app.static_folder)

    # handler = RotatingFileHandler('logs/app.log', maxBytes=10000, backupCount=1)
    # handler.setLevel(logging.INFO)
    # app.logger.addHandler(handler)

    app.run(use_debugger=app.debug, port=8000)
