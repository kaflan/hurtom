# coding: utf-8
import datetime
from datetime import date, datetime

from flask import (abort, flash, Flask, g, make_response, redirect,
                   render_template, request, url_for)
from flask.ext.babelex import gettext, lazy_gettext
from flask.ext.classy import FlaskView, route
from flask.ext.login import (current_user, login_required, login_user,
                             LoginManager, logout_user, UserMixin)

from app import app, db
from form import LoginForm, RegisterForm
from models import User
from rauth import OAuth2Service

__author__ = 'ihor'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'Login:index'
# login_manager.login_message = lazy_gettext('Bonvolu ensaluti por uzi tio paĝo.')
login_manager.login_message_category = 'info'
login_manager.session_protection = 'strong'


# login_user(user, remember=True)


#
#     mongo.db.users.save(example_user)


@login_manager.user_loader
def load_user(userid):
    return db.session.query(User).get(userid)


#
# Client ID
# 5d6035a213a5c92fe834
# Client Secret
# ed21f9eea8b9decab6bd834f6ae1a027b1b7b602

#
# facebook = OAuth2Service(
#     client_id='440483442642551',
#     client_secret='cd54f1ace848fa2a7ac89a31ed9c1b61',
#     name='facebook',
#     authorize_url='https://graph.facebook.com/oauth/authorize',
#     access_token_url='https://graph.facebook.com/oauth/access_token',
#     base_url='https://graph.facebook.com/')
#
#


# print(github.get_authorize_url())
# import ipdb; ipdb.set_trace()
# data = dict(code=code_, redirect_uri='http://localhost:8000/login/github')
# session = github.get_auth_session(data=data)
# session.get('user').json()


@app.context_processor
def push_current_user():
    '''adding user object to template context'''

    return {'user': current_user}


class Base(FlaskView):
    route_prefix = '/auth/'
    # def before_request(self, name):

    def index(self):
        return 'Index not defined ' + self.__class__.__name__


class BaseProvider(Base):
    oauth2_server = None

    def index(self):
        return redirect(self.oauth2_server.get_authorize_url())

    def callback(self):
        return self.__class__.__name__


class Github(BaseProvider):
    oauth2_server = OAuth2Service(
        client_id=app.config['GITHUB_ID'],
        client_secret=app.config['GITHUB_SECRET'],
        name='github',
        authorize_url='https://github.com/login/oauth/authorize',
        access_token_url='https://github.com/login/oauth/access_token',
        base_url='https://api.github.com/')

    def callback(self):
        code = request.args.get('code')

        if code is None:
            abort(404)

        data = dict(
            code=code, redirect_uri='http://localhost:8000/auth/github/callback/')
        session = self.oauth2_server.get_auth_session(data=data)
        json = session.get('user').json()
        user = current_user
        if not user.is_authenticated():
            user = db.session.query(User).filter_by(
                email=json['email']).first() or User()
            # avatar_url
            user.name = json['name']
            user.email = json['email']
            user.login = json['login']
        setattr(user, self.__class__.__name__.lower(), json)
        db.session.add(user)
        db.session.commit()
        flash('registered')
        login_user(user)
        return redirect('/')


class Register(Base):

    def index(self):
        if current_user.is_authenticated():
            flash('You already register!')
        return render_template('form.html', form=RegisterForm())

    def post(self):
        form = RegisterForm()
        if form.validate_on_submit():
            user = User()
            user.email = form.email.data
            user.login = form.login.data
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            # flash(lazy_gettext('You registered'))
        return render_template('form.html', form=form)


class Login(Base):
    # route_prefix = '/'
    # route_base = '/'

    def index(self):
        if current_user.is_authenticated():
            flash('You already loginned!')
        return render_template('form.html', form=LoginForm())

    def post(self):
        form = LoginForm()
        if form.validate_on_submit():
            user = db.session.query(User).filter_by(
                email=form.email.data).first()
            # flash(lazy_gettext('Logged in successfully.'))
            flash('loged')

            login_user(user, remember=form.remember_me.data)

            user.last_login = datetime.datetime.now()
            db.session.add(user)
            db.session.commit()
        return render_template('form.html', form=form)

    def forget_password(self):
        return 'forget'

    @login_required
    def logout(self):
        logout_user()
        flash('logouted')
        return redirect('/')


Github.register(app)
Login.register(app)
Register.register(app)
