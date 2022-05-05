from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, validators, SelectField
from wtforms.validators import DataRequired
try:
    from wtforms.fields.html5 import EmailField
except ModuleNotFoundError:
    from wtforms.fields import EmailField


class AdminRegisterForm(FlaskForm):
    name = StringField("Имя", validators=[DataRequired()])
    login = StringField("Логин", validators=[DataRequired(), validators.length(max=256)])
    email = EmailField("E-mail")
    occupation = StringField("Должность", validators=[DataRequired()])
    access = SelectField("Уровень допуска",
                         choices=[(0, "Уровень 0 (Для общего пользования)"),
                                  (1, "Уровень 1 (Для служебного пользования)"),
                                  (2, "Уровень 2 (Для ограниченного пользования)"),
                                  (3, "Уровень 3 (Секретно)"),
                                  (4, "Уровень 4 (Совершенно секретно)"),
                                  (5, "Уровень 5 (Таумиэль)")], default=0)
    password = PasswordField("Пароль", validators=[DataRequired()])
    repeat_password = PasswordField("Повторите пароль", validators=[DataRequired()])
    submit = SubmitField("Зарегистрироваться")
