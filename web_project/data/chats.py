from .db_session import SqlAlchemyBase

from sqlalchemy import orm
import sqlalchemy
import datetime

# Таблица линковки пользователей и чатов
connection = sqlalchemy.Table(
    # Название таблицы
    "connections",
    # Тип таблицы?
    SqlAlchemyBase.metadata,
    # Столбцы со "ссылками" ("ссылка" на пользователя и "ссылка" на беседу)
    sqlalchemy.Column("users", sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id")),
    sqlalchemy.Column("chats", sqlalchemy.Integer, sqlalchemy.ForeignKey("chats.id"))
)


# Таблица "объявления" бесед
class Chat(SqlAlchemyBase):
    __tablename__ = "chats"  # Название таблицы

    # Уникальный идентификатор беседы
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    # Название и локальная ссылка на изображение беседы
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False, default="Сохранённые сообщения")
    image = sqlalchemy.Column(sqlalchemy.String, default="../default_chat.svg")

    # Дата создания беседы
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    # Список состоящих в беседе пользователей
    users = orm.relation("User",           # "тип" добавляемого объекта
                         "connections",    # дополнительная таблица для линковки
                         backref="chats")  # Столбец в таблице линковки (User.chats -> [Chat...])

    def __repr__(self) -> str:
        return f"<Chat({self.id}) title={repr(self.title)}>"

    def __str__(self) -> str:
        return self.__repr__()
