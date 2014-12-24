#!/usr/bin/env python
# coding: utf-8

from __future__ import division, print_function, unicode_literals

from flask.ext.login import UserMixin

from app import app, db
from sqlalchemy import (Boolean, Column, create_engine, Date, DateTime,
                        ForeignKey, func, Integer, Numeric, select, Sequence,
                        String, Text, text, Unicode, UnicodeText)
from sqlalchemy.dialects.postgresql import ENUM, JSON
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property
from sqlalchemy.orm import (backref, column_property, object_session,
                            relationship, scoped_session, sessionmaker,
                            validates)
from sqlalchemy.ext.mutable import MutableDict

__author__ = 'ihor'


UText = UnicodeText
UString = Unicode
JSON = MutableDict.as_mutable(JSON)


#import bcrypt
#from slugify import slugify_ru


# self.slug = ((slug or slugify_ru(name, separator="_", to_lower=True))
#
#    @staticmethod
#    def set_password(password):
#        password = password.encode("utf-8")
#        return bcrypt.hashpw(password, bcrypt.gensalt(12))
#
#    def check_password(self, value=u""):
#        value = value.encode("utf-8")
#        return self.password == bcrypt.hashpw(value, self.password)
#
#


def create_base(engine=app.config['SQLALCHEMY_DATABASE_URI']):
    engine = create_engine(engine, convert_unicode=True, echo=True)
    Session.configure(bind=engine)
    Base.metadata.create_all(engine)
    return engine, Base, Session

Session = scoped_session(sessionmaker(bind=db.engine))  # autocommit=True,
# autoflush=True))


class Base(object):
    __abstract__ = True
    query = Session.query_property()

#    id = Column('id', Integer, primary_key=True)

#    id = Column("id", Integer, Sequence("country_id"), primary_key=True)

    @declared_attr
    def id(cls):
        # return Column("id", Integer, Sequence(cls.__tablename__ + "+_id"),
        # primary_key=True)
        return Column("id", Integer, primary_key=True)

    @hybrid_property
    def pk(self):
        return self.id

    @declared_attr
    def __tablename_easy__(cls):
        return cls.__name__.lower()

    @declared_attr
    def __tablename__(self):  # используеться для для имени в бд
        name = self.__name__

        def split_upper(line):
            for ind in range(1, len(line)):
                if line[ind].isupper():
                    if not line[ind + 1:].islower():
                        return [line[:ind].lower()] + split_upper(line[ind:])
                    else:
                        return [line[:ind].lower(), line[ind:].lower()]
            return [line.lower()]
        return "_".join(split_upper(name))

    @property
    def _sesion(self):
        return object_session(self)

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self


Base = declarative_base(cls=Base)

#
# example_user = dict(
#     login="sy",
#     email="sy@gmail.com",
#     name='ihor',
#     location='Kyiv',
#     github={},
#     last_visit=datetime.now(),
#     reg_data=datetime.now(),
#     avatar_image="",
# )

gravatar = app.extensions['gravatar']
class User(UserMixin, Base):

    @property
    def get_id(self):
        return str(self.email)
    email = Column(UString, nullable=False, unique=True, index=True)

    login = Column(UString(50))
    name = Column(UString(50))
    lastname = Column(UString(50))

    location = Column(UString)

    date_joined = Column(DateTime, default=func.now())
    last_login = Column(DateTime, default=func.now())

    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    use_avatar = Column(Boolean, default=False)

    github = Column(JSON)
    google = Column(JSON)

    avatar = db.Column(db.String(200))


    fullname = column_property(name + " " + lastname)

    # relations
    images = relationship("Image", backref="owner")




    @property
    def email_url(self):
        pass

class Project(Base):
    title = Column(UString)
    slug = Column(UString)
    description  = Column(UText)
    sum = Column(Integer, default=0)

    date_start = Column(DateTime, default=func.now())
    date_end = Column(DateTime, default=func.now())

    # relations
    images = relationship("Image", backref="project")


class Image(Base):
    filename = Column(String(200))
    owner_id = Column(Integer, ForeignKey(User.id))
    project_id = Column(Integer, ForeignKey(Project.id))
    project1_id = Column(Integer, ForeignKey(Project.id))


#
# @app.before_first_request
# def setup():
#     # Recreate database each time for demo
#     # Base.metadata.drop_all(bind=db.engine)
#     Base.metadata.create_all(bind=db.engine)
#     print('Create')
Base.metadata.create_all(bind=db.engine)
if __name__ == '__main__':
    engine, Base, Session = create_base()
    import ipdb
    ipdb.set_trace()
