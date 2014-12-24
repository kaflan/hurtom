__author__ = 'ihor'

from flask.ext.wtf import Form
from app import app
from models import User
from wtforms import (BooleanField, FieldList, FormField, HiddenField,
                     PasswordField, SelectMultipleField, StringField,
                     SubmitField, TextAreaField)
from wtforms.ext.sqlalchemy.orm import model_form
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, ValidationError

from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

class LoginForm(Form):
    email = EmailField(
        'Email', validators=[DataRequired(message="Username required")])
    password = PasswordField(
        'Password', validators=[DataRequired(message="Password required")])
    remember_me = BooleanField('Remember Me', default=False)
    submit = SubmitField('Sign in')

    def validate_password(form, field):
        try:
            user = User.query.filter(User.email == form.email.data).one()
        except (MultipleResultsFound, NoResultFound):
            raise ValidationError("Invalid user")
        if user is None:
            raise ValidationError("Invalid user")
        if not user.is_valid_password(form.password.data):
            raise ValidationError("Invalid password")
        form.user = user


class RegisterForm(Form):
    login = StringField('Login', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_again = PasswordField(
        'Password again', validators=[DataRequired()])
    submit = SubmitField('Register')
    def validate_email(form, field):
      user = User.query.filter(User.email == field.data).first()
      if user is not None:
          raise ValidationError("A user with that email already exists")


class ForgetForm(Form):
    email = EmailField('email')
    login = StringField('login')
