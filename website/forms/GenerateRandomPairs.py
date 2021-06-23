from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Email


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
