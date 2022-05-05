from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, validators
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    login = StringField("Логин", validators=[DataRequired(), validators.length(max=256)])
    password = PasswordField("Пароль", validators=[DataRequired()])
    remember_me = BooleanField("Запомни меня")
    submit = SubmitField("Войти")
