from .db_session import SqlAlchemyBase

from flask_login import UserMixin
import sqlalchemy
import datetime


# Таблица пользователей
class User(SqlAlchemyBase, UserMixin):
    __tablename__ = "users"  # Название таблицы

    # id, логин и e-mail пользователя
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    login = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False, index=True)
    email = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    # Имя и профессия пользователя
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    occupation = sqlalchemy.Column(sqlalchemy.String, default="D-class")

    # Локальная ссылка на иконку пользователя
    image = sqlalchemy.Column(sqlalchemy.String, default="../default_user.svg")

    # Пароль и уровень доступа пользователя
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    access = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    folowers = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    # Дата создания пользователя (вводить вручную не рекомендуется)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    def __repr__(self) -> str:
        return f"<User({self.id}) name={repr(self.name)} access={self.access}>"

    def __str__(self) -> str:
        return self.__repr__()
