from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from website.DB import session
from website.models import User


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
