from .db_session import SqlAlchemyBase

from sqlalchemy import orm
import sqlalchemy
import datetime


# Таблица хранения сообщений
class Message(SqlAlchemyBase):
    __tablename__ = "messages"  # Название таблицы

    # id сообщения и его текстовое содержание
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    text = sqlalchemy.Column(sqlalchemy.String, default='')

    # id отправителя и id беседы-получателя
    owner = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    chat_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("chats.id"))

    # Дата написания сообщения
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    # Объекты отправителя и получателя
    user = orm.relation("User", backref="messages")
    chat = orm.relation("Chat", backref="messages")

    def __repr__(self) -> str:
        return f"<Message({self.id}) text={repr(self.text)}>"

    def __str__(self) -> str:
        return f"<Message({self.id}) user={self.user} chat={self.chat} text={repr(self.text)}>"
