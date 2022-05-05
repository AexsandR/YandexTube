from .db_session import SqlAlchemyBase

from sqlalchemy import orm
import sqlalchemy
import datetime


# Таблица статей
class Article(SqlAlchemyBase):
    __tablename__ = "articles"  # Название таблицы

    # id и уровень допуска к статье
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    access = sqlalchemy.Column(sqlalchemy.Integer, default=0)

    # Название (для отображения на сайте) и локальная ссылка на статью
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False, unique=True)
    about = sqlalchemy.Column(sqlalchemy.String, default='')
    link = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    # Владелец статьи
    owner = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))

    # Дата создания статьи (вводить вручную не рекомендуется)
    create_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    # Объект владельца статьи
    user = orm.relation("User", backref="articles")
