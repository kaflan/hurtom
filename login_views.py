__author__ = 'ihor'
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

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'Login:index'
login_manager.login_message = lazy_gettext('Login message')
login_manager.login_message_category = 'info'
login_manager.session_protection = 'strong'


@login_manager.user_loader
def load_user(userid):
    return db.session.query(User).get(userid)


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
    user_name = "me"
    params = None

    @property
    def name(self):
        return self.__class__.__name__

    def index(self):
        return redirect(self.oauth2_server.get_authorize_url())

    def callback(self):
        code = request.args.get('code')
        print(code)

        if code is None:
            abort(404)

        data = dict(
            code=code, redirect_uri=url_for(self.name + ':callback'))

        import ipdb
        ipdb.set_trace()
        session = self.oauth2_server.get_auth_session(data=data)

        json = session.get('me').json()
        user = current_user
        if not user.is_authenticated():
            user = db.session.query(User).filter_by(
                email=json['email']).first() or User()
            # avatar_url
            user.name = json['name']
            user.email = json['email']
            user.login = json['login']
        setattr(user, self.name.lower(), json)
        db.session.add(user)
        db.session.commit()
        flash('registered')
        login_user(user)
        return redirect('/')


class Github(BaseProvider):
    oauth2_server = OAuth2Service(
        client_id=app.config['GITHUB_ID'],
        client_secret=app.config['GITHUB_SECRET'],
        name='github',
        authorize_url='https://github.com/login/oauth/authorize',
        access_token_url='https://github.com/login/oauth/access_token',
        base_url='https://api.github.com/')


class Facebook(BaseProvider):
    base_url = 'https://www.facebook.com/dialog/oauth'

    oauth2_server = OAuth2Service(name='facebook',
                                  # authorize_url=base_url,
                                  # access_token_url=base_url +'/access_token',
                                  client_id=app.config['FACEBOOK_ID'],
                                  client_secret=app.config['FACEBOOK_SECRET'],
                                  # base_url=base_url,
                                  authorize_url='https://graph.facebook.com/oauth/authorize',
                                  access_token_url='https://graph.facebook.com/oauth/access_token',
                                  base_url='https://graph.facebook.com/'
                                  )

    def index(self):
        params = self.params or {'scope': 'read_stream',
                                 'response_type': 'code',
                                 'redirect_uri': url_for("Facebook:callback", _external=True)}
        print(url_for("Facebook:callback", _external=True))
        return redirect(self.oauth2_server.get_authorize_url(**params))


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
# Facebook.register(app)
Login.register(app)
Register.register(app)
