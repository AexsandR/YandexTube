from .db_session import SqlAlchemyBase

from sqlalchemy import orm
import sqlalchemy
import datetime


# Таблица хранения сообщений
class Comment(SqlAlchemyBase):
    __tablename__ = "Comment"  # Название таблицы

    # id сообщения и его текстовое содержание
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    text = sqlalchemy.Column(sqlalchemy.String, default='')

    # id отправителя и id беседы-получателя
    owner = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    video_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("video.id"))

    # Дата написания сообщения
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    # Объекты отправителя и получателя

