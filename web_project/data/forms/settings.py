from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, validators
from wtforms.validators import DataRequired
try:
    from wtforms.fields.html5 import EmailField
except ModuleNotFoundError:
    from wtforms.fields import EmailField


class SettingsForm(FlaskForm):
    name = StringField("Ваше имя:", validators=[DataRequired()])
    login = StringField("Ваш логин:", validators=[DataRequired(), validators.length(max=256)])
    email = EmailField("Ваш e-mail:")
    password = PasswordField("Пароль:")
    image = FileField("Ваша иконка:")

    submit = SubmitField("Изменить и сохранить")
