import smtplib

my_email= 'flask_test@mail.ua'

my_email_password = 'qwerty'

import email.utils
from email.mime.text import MIMEText


def send_email(to_email,to_name, from_name="Robot",
               subject="", body="", from_email=my_email):
    # Create the message
    msg = MIMEText(body)
    msg['To'] = email.utils.formataddr((to_name, to_email))
    msg['From'] = email.utils.formataddr((from_name, from_email))
    msg['Subject'] = subject
    server = smtplib.SMTP('smtp.mail.ru', 2525)
    server.ehlo()
    server.starttls()
    server.login(my_email, my_email_password)
    server.sendmail(from_email,[to_email], msg.as_string())
    server.quit()

# send_email(to_email=,
#            to_name='lolicon',
#            subject='sdfsdf',
#            body='body')

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