from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo


class SubmitSendingEmail(FlaskForm):
    email_title = StringField(
        'Email title',
        validators=[
            DataRequired(),
            Length(min=2, max=20)
        ]
    )
    email_body = StringField(
        'Email body',
        validators=[
            DataRequired(),
            Length(min=2, max=200)
        ]
    )
    submit = SubmitField(
        'Submit'
    )


class UpdatePassword(FlaskForm):
    password = PasswordField(
        'New Password',
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
        'Update Password'
    )
