from flask import (Flask, g, make_response, render_template,
                   send_from_directory, url_for)
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


@app.route('/')
@login_required
def index():
    return '<a href="{}"> Login</a>'.format(url_for('Login:index')) +\
           '<a href="{}"> Register</a>'.format(url_for('Register:index'))


@app.route('/media/<path:filename>')
def media(filename):
    return send_from_directory(app.static_folder, filename)


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


@app.errorhandler(500)
def page_not_found500(error):
    return render_template("500.html"), 500
