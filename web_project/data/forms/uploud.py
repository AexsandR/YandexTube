from flask_wtf import FlaskForm
from wtforms import IntegerField, PasswordField, BooleanField, SubmitField, StringField, FileField
from flask_wtf.file import FileField, FileRequired
from wtforms.validators import DataRequired


class Uploud_forms(FlaskForm):
    photo_user = FileField("выбрать постер для видео", validators=[FileRequired()])
    video_user = FileField("выбрать видео",validators=[FileRequired()])
    name = StringField('название для видео', validators=[DataRequired()])
    submit = SubmitField('загрузить')
