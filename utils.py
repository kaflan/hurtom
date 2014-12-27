import email.utils
import os.path
import smtplib
import sys
from email.mime.text import MIMEText

from app import app


class ObjectDict(dict):

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        self[name] = value

    @property
    def __str__(self):
        return "ObjectDict"

    def __repr__(self):
        return self.__str__
config = ObjectDict(app.config)


def send_email(to_email, to_name, from_name="Robot",
               subject="", body="", from_email=config.EMAIL):
    # Create the message
    msg = MIMEText(body)
    msg['To'] = email.utils.formataddr((to_name, to_email))
    msg['From'] = email.utils.formataddr((from_name, from_email))
    msg['Subject'] = subject
    server = smtplib.SMTP('smtp.mail.ru', 2525)
    server.ehlo()
    server.starttls()
    server.login(config.EMAIL, config.EMAIL_PASSWORD)
    server.sendmail(from_email, [to_email], msg.as_string())
    server.quit()


def install_secret_key(app, filename='secret_key.txt'):
    """Configure the SECRET_KEY from a file
    in the instance directory.

    If the file does not exist, print instructions
    to create it from a shell with a random key,
    then exit.

    """
    filename = os.path.join(app.instance_path, filename)
    try:
        app.config['SECRET_KEY'] = open(filename, 'rb').read()
    except IOError:
        print('Error: No secret key. Create it with:')
        if not os.path.isdir(os.path.dirname(filename)):
            print('mkdir -p', os.path.dirname(filename))
        print('head -c 24 /dev/urandom >', filename)
        sys.exit(1)
