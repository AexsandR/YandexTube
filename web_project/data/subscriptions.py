from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import sqlalchemy
import datetime


# Таблица пользователей
class Subscriptions(SqlAlchemyBase, UserMixin):
    __tablename__ = "subscriptions"  # Название таблицы
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    who_subscribed = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    who_did_you_subscribe_to = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))