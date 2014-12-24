__author__ = 'ihor'
from  app import app, mongo

from flask import Flask, g, render_template, make_response, url_for,redirect
from flask.ext.login import LoginManager

from flask.ext.classy import FlaskView
from flask.ext.login import LoginManager, login_required, login_user, current_user,logout_user
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'Login:index'
login_manager.login_message = 'Bonvolu ensaluti por uzi tio paĝo.'
login_manager.login_message_category = 'info'
login_manager.session_protection = "strong"


# login_user(user, remember=True)

from flask.ext.login import UserMixin

class ProxyUser(UserMixin):
   is_authenticated = True
   is_active = True
   is_anonymous = True

   def get_id(self):
       return "3"

@login_manager.user_loader
def load_user(userid):
    return ProxyUser() # User.get(userid)



from rauth import OAuth2Service
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
    client_id='5d6035a213a5c92fe834',
    client_secret='ed21f9eea8b9decab6bd834f6ae1a027b1b7b602',
    name='github',
    authorize_url='https://github.com/login/oauth/authorize',
    access_token_url='https://github.com/login/oauth/access_token',
    base_url='https://api.github.com/')

print(github.get_authorize_url())
#data = dict(code=code_, redirect_uri='http://localhost:8000/login/github')
# session = github.get_auth_session(data=data)
 # session.get('user').json()




@login_required
@app.route('/')
def hello_world():
    return 'Hello World!'+url_for('Login:index')

class Base(FlaskView):
    route_prefix = '/login/'
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

class Login(FlaskView):
    # route_prefix = '/login/'
    # route_base = '/'

    def index(self):
        return 'lol'

    def post(self):
        return 'post'

    def success(self):
        return 'success'

    @login_required
    def logout(self):
        #logout_user()
        print(url_for('Login:success_logout'))
        return redirect(url_for('Login:success_logout'))

    def success_logout(self):
        return "you logout"

# Base.register(app)
Github.register(app)
Login.register(app)
