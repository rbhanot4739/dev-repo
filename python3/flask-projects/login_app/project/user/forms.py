from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import (PasswordField, StringField, SubmitField, TextAreaField,
                     ValidationError)
from wtforms.fields import BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email, EqualTo, length
from flask_wtf.file import FileField, FileAllowed

from ..models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')
    remember_me = BooleanField('Remember Me')


class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(message='Username can\'t be empty'),
        length(min=4, max=10)])
    email = EmailField('Email', validators=[
        DataRequired(message='Email can\'t be blank'),
        Email(message='Invalid email format')])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(),
                                                 EqualTo('password',
                                                         'Passwords must match')])
    submit = SubmitField('Register')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first() is not None:
            raise ValidationError("This username already exists !")


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About Me', validators=[DataRequired(),
                                                     length(min=10, max=1000)])
    profile_picture = FileField('Profile Picture', validators=[FileAllowed([
        'jpg', 'png'])])
    update = SubmitField('Update')

    def validate_username(self, field):
        user = User.query.filter_by(username=field.data).first()
        if user and user.username != current_user.username:
            raise ValidationError("Username already exists !")
