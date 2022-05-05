from flask_wtf import FlaskForm
from wtforms import IntegerField, PasswordField, BooleanField, SubmitField, StringField
from wtforms.validators import DataRequired


class Video_form(FlaskForm):
    comment = StringField('', validators=[DataRequired()])
    send_comment = SubmitField('send comment')

