from flask_wtf import FlaskForm
from wtforms import IntegerField, PasswordField, BooleanField, SubmitField, StringField
from wtforms.validators import DataRequired


class RegForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    Reapeat_password = PasswordField('Reapeat:password', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Submit')