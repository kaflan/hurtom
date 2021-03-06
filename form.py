from flask.ext.babelex import gettext, lazy_gettext
from flask.ext.wtf import Form

from app import app
from models import User
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from wtforms import (BooleanField, FieldList, FormField, HiddenField,
                     PasswordField, SelectMultipleField, StringField,
                     SubmitField, TextAreaField)
from wtforms.ext.sqlalchemy.orm import model_form
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, EqualTo, ValidationError


class LoginForm(Form):
    email = EmailField(
        lazy_gettext('Email'), validators=[DataRequired(message=lazy_gettext("Email required"))])
    password = PasswordField(
        lazy_gettext('Password'), validators=[DataRequired(message=lazy_gettext("Password required"))])
    remember_me = BooleanField(lazy_gettext('Remember Me'), default=False)
    submit = SubmitField(lazy_gettext('Sign in'))

    def validate_password(form, field):
        try:
            user = User.query.filter(User.email == form.email.data).one()
        except (MultipleResultsFound, NoResultFound):
            raise ValidationError(
                lazy_gettext("User with this email do not exists."))
        if user is None:
            raise ValidationError(
                lazy_gettext("User with this email do not exists."))
        if not user.check_password(form.password.data):
            raise ValidationError(lazy_gettext("Invalid password"))
        form.user = user


class RegisterForm(Form):
    login = StringField(lazy_gettext('Login'))
    # login = StringField(lazy_gettext('Login'), validators=[DataRequired()])
    email = EmailField(lazy_gettext('Email'), validators=[DataRequired()])
    password = PasswordField(
        lazy_gettext('Password'), validators=[DataRequired()])
    password_again = PasswordField(
        lazy_gettext('Password again'), validators=[
            DataRequired(),
            EqualTo("password", message=lazy_gettext("Passwords do not match"))
        ])
    submit = SubmitField(lazy_gettext('Register'))

    def validate_email(form, field):
        user = User.query.filter(User.email == field.data).first()
        if user is not None:
            raise ValidationError(
                lazy_gettext("A user with that email already exists"))


class ForgetForm(Form):
    email = EmailField(lazy_gettext('Email'))
    login = StringField(lazy_gettext('Login'))


class ResetPasswordForm(Form):

    ''
    # token
    # email
    # password


class ChangePassword(Form):
    old_password = PasswordField(lazy_gettext('Password'), validators=[
        DataRequired()])

    password = PasswordField(lazy_gettext('Password'), validators=[
        DataRequired()])

    confirm_password = PasswordField(lazy_gettext('Confirm password'), validators=[
        DataRequired(),
        EqualTo('password', message=lazy_gettext('Passwords must match'))])
