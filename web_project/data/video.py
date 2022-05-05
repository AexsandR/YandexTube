from .db_session import SqlAlchemyBase

from flask_login import UserMixin
import sqlalchemy
import datetime





# Таблица пользователей
class Video(SqlAlchemyBase, UserMixin):
    __tablename__ = "video"  # Название таблицы
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    owner = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    views = sqlalchemy.Column(sqlalchemy.Integer, default=0)

