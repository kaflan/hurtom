from flask import Flask
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, g, render_template, make_response
from flask.ext.login import LoginManager
from flask.ext.pymongo import PyMongo
from flask.ext.gravatar import Gravatar


app = Flask(__name__)
app.config.from_object('config')


mongo = PyMongo(app)


# http://flask.pocoo.org/docs/0.10/errorhandling/

gravatar = Gravatar(app,
                    size=100,
                    rating='g',
                    default='retro',
                    force_default=False,
                    force_lower=False,
                    use_ssl=False,
                    base_url=None)
from views import *
from login_views import *

if __name__ == '__main__':
    handler = RotatingFileHandler('foo.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    print(app.url_map)

    use_debugger=False
    if app.debug:
        use_debugger=True
    app.run(use_debugger=use_debugger,port = 8000)



# @app.route('/user/<username>')
# def user_profile(username):
#     user = mongo.db.users.find_one_or_404({'_id': username})
#     return render_template('user.html',
#         user=user)
#
# @app.route('/<ObjectId:task_id>')
# def show_task(task_id):
#     task = mongo.db.tasks.find_one_or_404(task_id)
#     return render_template('task.html', task=task)
