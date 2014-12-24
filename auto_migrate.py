__author__ = 'ihor'
from app import app
from flask_alembic import Alembic
alembic = Alembic()
alembic.init_app(app)
with app.app_context():
    alembic.revision('')
    alembic.upgrade()
