#!/usr/bin/env python3
from app import app, db
from flask.ext.script import Manager

manager = Manager(app)

from flask_alembic import Alembic


alembic = Alembic()
alembic.init_app(app)

@manager.command
def automigrate(name=None):
    with app.app_context():
        import ipdb; ipdb.set_trace()
        alembic.revision(name or "Init")
        alembic.upgrade()

if __name__ == '__main__':
    manager.run()
