from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from .DB import session
from .models import User


class RegistrationForm(FlaskForm):
    username = StringField(
        'username',
        validators=[
            DataRequired(),
            Length(min=2, max=20)
        ]
    )
    email = StringField(
        'email',
        validators=[
            DataRequired(),
            Email()
        ]
    )
    password = PasswordField(
        'password',
        validators=[
            DataRequired()
        ]
    )
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired(),
            EqualTo('password')
        ]
    )
    submit = SubmitField(
        'Sign Up'
    )

    def validate_username(self, username):
        user_name = session.query(User).filter_by(username=username.data).first()
        if user_name:
            raise ValidationError('This name is taken.')

    def validate_email(self, email):
        email = session.query(User).filter_by(email=email.data).first()
        if email:
            raise ValidationError('This email is taken.')


class LoginForm(FlaskForm):
    email = StringField(
        'email',
        validators=[
            DataRequired(),
            Email()
        ]
    )
    password = PasswordField(
        'password',
        validators=[
            DataRequired()
        ]
    )
    remember = BooleanField(
        'Remember Me'
    )
    submit = SubmitField(
        'Login'
    )


class GenerateRandomPairsForm(FlaskForm):
    random_person_name = StringField(
        'name',
        validators=[
            DataRequired(),
            Length(min=2, max=20)
        ]
    )
    random_person_email = StringField(
        'email',
        validators=[
            DataRequired(),
            Email()
        ]
    )
    add_item = SubmitField(
        'Add Item'
    )
    remove_item = SubmitField(
        'Remove Item'
    )
    submit = SubmitField(
        'Submit'
    )
