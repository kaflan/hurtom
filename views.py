from flask import Flask, g, make_response, render_template, url_for
from flask.ext.classy import FlaskView
from flask.ext.login import login_required, LoginManager
from werkzeug import secure_filename

from app import app
from form import LoginForm

__author__ = 'ihor'


@app.route('/test')
def test():
    return render_template('base.html')


@app.route('/form/', methods=['post', 'get'])
def form():
    form = LoginForm()
    if form.validate_on_submit():
        print(form.data)
    else:
        print(form.errors)
    return render_template('form.html', form=form)


@login_required
@app.route('/')
def index():

    # print(tuple(mongo.db.users.find()))
    return 'Hello World!' + url_for('Login:index')
