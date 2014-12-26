# coding: utf-8
from datetime import date, datetime
from flask.ext.babelex import lazy_gettext
from flask import (flash, Flask, g, make_response, redirect, render_template,
                   request, url_for)
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
login_manager.login_message = 'Bonvolu ensaluti por uzi tio paĝo.'
login_manager.login_message_category = 'info'
login_manager.session_protection = "strong"


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
github = OAuth2Service(
    client_id='db87c735a6ce6faaa2e1',
    client_secret='90516141b451cc3e2ad7a8e55f4f9711d86813b2',
    name='github',
    authorize_url='https://github.com/login/oauth/authorize',
    access_token_url='https://github.com/login/oauth/access_token',
    base_url='https://api.github.com/')

print(github.get_authorize_url())
# import ipdb; ipdb.set_trace()
#data = dict(code=code_, redirect_uri='http://localhost:8000/login/github')
# session = github.get_auth_session(data=data)
# session.get('user').json()


class Base(FlaskView):
    route_prefix = '/auth/'
    # def before_request(self, name):

    def index(self):
        return 'Index'

    def callback(self):
        return 'callback'


class Github(Base):

    def index(self):
        return 'Index'

    def callback(self):
        return 'github'

class Register(Base):
    def index(self):
        return render_template('form.html', form=RegisterForm())

    def post(self):
        form = RegisterForm()
        if form.validate_on_submit():
            user = User()
            user.email =  form.email.data
            user.login =  form.login.data
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            login_user(user=user)
            flash(lazy_gettext("You registered"))
            return redirect(url_for('Login:success'))
        return render_template('form.html', form=form)


class Login(Base):
    # route_prefix = '/login/'
    # route_base = '/'

    def index(self):
        return render_template('form.html', form=LoginForm())

    def post(self):
        form = LoginForm()
        if form.validate_on_submit():
            print(form.data)  # success
            print(User.query.all())
            user = db.session.query(User).first(form.email)
            print(user)
            import ipdb; ipdb.set_trace()
            flash(lazy_gettext("Logged in successfully."))

            # login_user(user=user)
        else:
            print(form.errors)
        # import ipdb; ipdb.set_trace()
        print(form.email.flags)
        return render_template('form.html', form=form)

    def success(self):
        return 'success logined'

    @login_required
    def logout(self):
        logout_user()
        return redirect(url_for('Login:success_logout'))

    def success_logout(self):
        return "you logout"

# Base.register(app)
Github.register(app)
Login.register(app)
Register.register(app)
