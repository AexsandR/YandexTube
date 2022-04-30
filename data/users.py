from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import sqlalchemy
import datetime


# Таблица пользователей
class User(SqlAlchemyBase, UserMixin):
    __tablename__ = "users"  # Название таблицы

    # id, логин и e-mail пользователя
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    email = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # Имя и профессия пользователя
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    image = sqlalchemy.Column(sqlalchemy.String, default='img/Users/logo-user.png')
    # Пароль и уровень доступа пользователя
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    folowers = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    # Дата создания пользователя (вводить вручную не рекомендуется)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
