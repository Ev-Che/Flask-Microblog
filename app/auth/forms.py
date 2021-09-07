from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from flask_babel import _, lazy_gettext as _l
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

from app.services import get_user_by_username, get_user_by_email


class LoginForm(FlaskForm):
    username = StringField(_l('Username'),
                           validators=[DataRequired()])
    password = PasswordField(_l('Password'),
                             validators=[DataRequired()])
    remember_me = BooleanField(_l('Remember Me'))
    submit = SubmitField(_l('Sign In'))


class RegistrationForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    password2 = PasswordField(_l('Repeat password'),
                              validators=[DataRequired(),
                                          EqualTo('password')])
    submit = SubmitField(_l('Register'))

    def validate_username(self, username):
        user = get_user_by_username(username=username.data)
        if user is not None:
            raise ValidationError(_l('Please user a different username.'))

    def validate_email(self, email):
        user = get_user_by_email(email=email.data)
        if user is not None:
            raise ValidationError(_l('Please user a different email address.'))


class ResetPasswordRequestForm(FlaskForm):
    email = StringField(_l('Email'), validators=[DataRequired(),
                                                 Email()])
    submit = SubmitField(_l('Request Password Reset'))


class ResetPasswordForm(FlaskForm):
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    password2 = PasswordField(
        _l('Repeat password'),
        validators=[DataRequired(), EqualTo('password')]
    )
    submit = SubmitField(_l('Request Password Reset'))
