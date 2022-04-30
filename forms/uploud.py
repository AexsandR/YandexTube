from flask_wtf import FlaskForm
from wtforms import IntegerField, PasswordField, BooleanField, SubmitField, StringField, FileField
from flask_wtf.file import FileField, FileRequired
from wtforms.validators import DataRequired


class Uploud_forms(FlaskForm):
    file = FileField("выбрать постер для видео", validators=[FileRequired()])
    file1 = FileField("выбрать видео",validators=[FileRequired()])
    name = StringField('название для видео', validators=[DataRequired()])
    submit = SubmitField('загрузить')
