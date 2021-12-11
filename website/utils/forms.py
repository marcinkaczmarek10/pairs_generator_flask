from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class SubmitSendingEmail(FlaskForm):
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
