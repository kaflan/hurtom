#!/usr/bin/env python3
import logging
from logging.handlers import RotatingFileHandler

from flask import Flask, g, make_response, render_template
from flask.ext.gravatar import Gravatar
from flask.ext.login import LoginManager

from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CsrfProtect

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

CsrfProtect(app)


# http://flask.pocoo.org/docs/0.10/errorhandling/

gravatar = Gravatar(app,
                    size=100,
                    rating='g',
                    default='retro',
                    force_default=False,
                    force_lower=False,
                    use_ssl=False,
                    base_url=None)
if True:
    from login_views import *
    from views import *
    from models import Base


if __name__ == '__main__':
    print(app.url_map)

    # handler = RotatingFileHandler('logs/app.log', maxBytes=10000, backupCount=1)
    # handler.setLevel(logging.INFO)
    # app.logger.addHandler(handler)

    app.run(use_debugger=app.debug, port=8000)
