from abc import ABC, abstractmethod
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, IntegerField

class BaseForm(ABC, FlaskForm):
