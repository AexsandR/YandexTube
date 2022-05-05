from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, validators
from wtforms.validators import DataRequired


class Msg_form(FlaskForm):
    label_msg = StringField("Логин", validators=[DataRequired(), validators.length(max=256)])
    submit = SubmitField("отправить")
