from flask_wtf import Form
from wtforms import StringField, BooleanField, SubmitField, validators
from wtforms.validators import Required


class NameForm(Form):
        name = StringField('What is your name?', validators=[Required()])
        email = StringField('email?', validators=[Required()])
        submit = SubmitField('Submit')