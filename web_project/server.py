import flask
from flask import request, jsonify, Blueprint
from data.__all_models import *  # импорт всех orm-моделей
from data import db_session


def verify_email(email: str) -> bool:
    return bool(email)


blueprint = flask.Blueprint(
    "server",
    __name__,
    template_folder="templates"
)


@blueprint.route("/api/send/messages", methods=["POST"])
def send_message():
    """
    {
        "type": "message",
        "content": {
            "owner": owner_id,
            "chat_id": chat_id,
            "text": message_text
        }
    }
    """
    if not request.json:
        return jsonify({'code': 204, 'error': 'Empty request'})
    try:
        db = db_session.create_session()
        data = request.json
        if "type" in data:
            # Проверка типа (сообщение)
            if data["type"].lower() == "message":
                # Проверка правильности контента
                if "content" in data and isinstance(data["content"], dict):
                    content = data["content"]
                    # Проверка правильности в контенте
                    if len(content) == 3 and "owner" in content and "chat_id" in content and \
                            "text" in content and isinstance(content["owner"], int) and \
                            isinstance(content["chat_id"], int) and isinstance(content["text"], str):
                        message = Message()
                        message.owner = content['owner']  # отправитель
                        message.chat_id = content['chat_id']  # id чата
                        message.text = content['text']  # текст сообщения

                        db.add(message)
                        db.commit()
                    else:
                        raise SyntaxError("Wrong syntax for 'content' tag")
                else:
                    raise SyntaxError("Wrong syntax for 'content' tag")
            else:
                raise TypeError("Wrong syntax for 'type' tag")
    except Exception as error:
        return jsonify({"code": 666, "error": error})
    return jsonify({"code": 200, "error": 'OK'})


@blueprint.route("/api/get/messages", methods=["POST"])
def get_messages():
    """
    {
        "count": message_count,
        "chat_id": chat_id
    }
    """
    if not request.json:
        return jsonify({"status": 204, "error": "Empty request!"})

    data = request.json

    # Проверка правильности запроса
    if len(data) == 3 and "count" in data and "chat_id" in data and "last_message" in data and \
            isinstance(data["count"], int) and isinstance(data["chat_id"], int) and \
            isinstance(data["last_message"], int) and \
            data["count"] > 0 and data["chat_id"] >= 0:
        db = db_session.create_session()
        messages = db.query(Message).filter(
            (Message.chat_id == data["chat_id"]) & (Message.id > data["last_message"])).all()[
                   -data["count"]:]
        answer = [{"id": message.id, "owner": message.owner, "text": message.text,
                   "user_image": message.user.image} for message in messages]

        return jsonify({"status": 200, "error": "OK", "content": answer})
    else:
        return jsonify({"status": 666, "error": "Wrong syntax of request"})
