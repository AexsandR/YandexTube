from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, TextAreaField
from wtforms.validators import DataRequired


class ArticleAddForm(FlaskForm):
    link = StringField("Ссылка на статью:", validators=[DataRequired()])

    title = StringField("Название статьи:")
    description = TextAreaField("Описание статьи:")
    file = FileField("Ваша статья:", validators=[DataRequired()])

    submit = SubmitField("Добавить и сохранить")
