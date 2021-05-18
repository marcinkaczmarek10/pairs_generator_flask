from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from website.database.DB import session
from website.database.models import User


class ResetPasswordSubmitForm(FlaskForm):
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(),
        ]
    )
    submit = SubmitField(
        'Reset Password'
    )

    def validate_email(self, email):
        email = session.query(User).filter_by(email=email.data).first()
        if not email:
            raise ValidationError('This email does not exist')


class ResetPasswordForm(FlaskForm):
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
        'Reset Password'
    )
