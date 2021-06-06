from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email


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
