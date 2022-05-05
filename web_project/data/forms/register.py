from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, validators
from wtforms.validators import DataRequired
try:
    from wtforms.fields.html5 import EmailField
except ModuleNotFoundError:
    from wtforms.fields import EmailField


class RegisterForm(FlaskForm):
    name = StringField("Имя", validators=[DataRequired()])
    login = StringField("Логин", validators=[DataRequired(), validators.length(max=256)])
    email = EmailField("E-mail", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    repeat_password = PasswordField("Повторите пароль", validators=[DataRequired()])
    remember_me = BooleanField("Запомни меня")
    submit = SubmitField("Зарегистрироваться")
