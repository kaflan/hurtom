__author__ = 'ihor'
from  app import app
from flask.ext.classy import FlaskView


@app.route('/test')
def test():
    return render_template('test.html')
