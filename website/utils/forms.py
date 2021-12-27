from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError
from website.database.DB import SessionFactory
from website.database.models import User


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
        user_name = SessionFactory.session.query(User).filter_by(username=username.data).first()
        if user_name:
            raise ValidationError('This name is taken.')

    def validate_email(self, email):
        email = SessionFactory.session.query(User).filter_by(email=email.data).first()
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


class SubmitSendingEmailForm(FlaskForm):
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


class UpdatePasswordForm(FlaskForm):
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
        email = SessionFactory.session.query(User).filter_by(email=email.data).first()
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


class GenerateRandomPairsForm(FlaskForm):
    person_name = StringField(
        'name',
        validators=[
            DataRequired(),
            Length(min=2, max=20)
        ]
    )
    person_email = StringField(
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
