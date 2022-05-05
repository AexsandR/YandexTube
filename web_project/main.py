import os.path

from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, redirect, abort
from werkzeug.utils import secure_filename

from data.forms.__all_forms import *  # импорт всех форм
from data.__all_models import *  # импорт всех orm-моделей
from data import db_session
from random import randint
from server import *
import datetime
from YandexTube import channel, main_page_YandexTube, search, subscribe_describe, subscriptions, upload_video, \
    wath_video

app = Flask(__name__)

login_manager = LoginManager()
app.config["SECRET_KEY"] = "scp-foundation_secret_key"
login_manager.init_app(app)
app.register_blueprint(blueprint)
app.register_blueprint(main_page_YandexTube.blueprint)
app.register_blueprint(channel.blueprint)
app.register_blueprint(search.blueprint)
app.register_blueprint(subscribe_describe.blueprint)
app.register_blueprint(subscriptions.blueprint)
app.register_blueprint(upload_video.blueprint)
app.register_blueprint(wath_video.blueprint)


@app.before_request
def search():
    if request.method == 'POST':
        if 'search' in request.form:
            res = request.form['search']
            res = res.split()
            res = '_'.join(res)
            return redirect(f'/search/{res}')


@login_manager.user_loader
def load_user(user_id):
    """Подгрузка пользователя"""
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    """Страница выхода из аккаунта"""
    logout_user()
    return redirect("/")


# Обработка некоторых ошибок
@app.errorhandler(400)
@app.route("/400")
def error_400(error=None):
    return render_template("400.html", title="Bad Request")


@app.errorhandler(401)
@app.route("/401")
def error_401(error=None):
    """Отображение ошибки "Незарегистрированный пользователь" (401)"""
    return render_template("401.html", title="Доступ запрещён!", randint=randint)


@app.errorhandler(403)
@app.route("/403")
def error_403(error=None):
    if isinstance(error.description, int):
        return render_template("403_article.html", title="Отказано в доступе!",
                               access=error.description, ip=request.remote_addr)
    return render_template("403.html", title="Доступ запрещён!")


@app.errorhandler(404)
@app.route("/404")
def error_404(error="The requested URL was not found on the server. If you entered "
                    "the URL manually please check your spelling and try again."):
    """Отображение ошибки "Страница не найдена" (404)"""
    if error.description != "The requested URL was not found on the server. If you entered " \
                            "the URL manually please check your spelling and try again.":
        return render_template("404.html", title=error.description)
    return render_template("404.html", title="Страница не найдена!")


@app.errorhandler(413)
@app.route("/413")
def error_413(error=None):
    return render_template("413.html", title="Файл слишком большой")


@app.errorhandler(418)
@app.route("/418")
def error_418(error=None):
    return render_template("418.html", title="I'm a teapot!")


@app.errorhandler(500)
@app.route("/500")
def error_500(error):
    return render_template("500.html", title="Упс...что-то сломалось")


# Авторизация и Регистрация
@app.route("/login/", methods=["GET", "POST"])
def login():
    """Страница входа в свой аккаунт"""
    # Коды "ошибок":
    # 0 - никаких ошибок
    # 1 - некоректный пользователь
    # 2 - неверный пароль

    form = LoginForm()  # реализуем форму входа

    # форма заполнена относительно-корректно
    if form.validate_on_submit():
        db_sess = db_session.create_session()  # создаём сессию
        user = db_sess.query(User).filter(User.login == form.login.data.strip()).first()

        # Пользователь не существует
        if not user:
            return render_template("login.html", title="Авторизация",
                                   message="Пользователь не существует!", form=form,
                                   error=1)
        elif check_password_hash(user.hashed_password, form.password.data):
            # Авторизуем пользователя
            login_user(user, form.remember_me.data)
            return redirect('/')
        # Неверный пароль
        return render_template("login.html", title="Авторизация",
                               message="Неверный пароль!", form=form,
                               error=2)
    # Первый вход, никаких данных
    return render_template("login.html", title="Авторизация", form=form,
                           error=0)


@app.route("/register/", methods=["GET", "POST"])
def register():
    """Страница регистрации пользователя"""
    # Коды "ошибок":
    # 0 - никаких ошибок
    # 1 - пользователь уже существует
    # 2 - неверный e-mail
    # 3 - пароли не совпадают

    form = RegisterForm()

    # форма заполнена относительно-корректно
    if form.validate_on_submit():
        db_sess = db_session.create_session()  # создаём сессию
        user = db_sess.query(User).filter(User.login == form.login.data.strip()).first()

        # Пользователь не существует - это хорошо
        if not user:
            # E-mail настоящий
            if verify_email(form.email.data):
                if form.password.data == form.repeat_password.data:
                    # Регистрируем пользователя
                    user = User()
                    chat = Chat()

                    chat.title = "Сохранённые сообщения"

                    user.name = form.name.data
                    user.login = form.login.data
                    user.email = form.email.data
                    user.hashed_password = generate_password_hash(form.password.data)
                    user.chats.append(chat)

                    db_sess.add(user)
                    db_sess.commit()

                    # авторизуем пользователя
                    login_user(user)

                    return redirect('/')
                else:
                    # Пароли не совпадают - ошибка
                    return render_template("register.html", title="Регистрация", form=form, error=3,
                                           message="Пароли не совпадают!")
            else:
                # Ошибка e-mail
                return render_template("register.html", title="Регистрация", form=form, error=2,
                                       message="Некоректный e-mail!")
        else:
            # Пользователь уже существует - ошибка
            return render_template("register.html", title="Регистрация", form=form, error=1,
                                   message="Пользователь уже существует!")
    # Первый вход, никаких данных
    return render_template("register.html", title="Регистрация", form=form, error=0)


@app.route("/admin/register", methods=["GET", "POST"])
@login_required
def admin_register():
    """Место Окончательной Регистрации Граждан"""
    # Коды "ошибок":
    # 0 - никаких ошибок
    # 1 - пользователь уже существует
    # 2 - неверный e-mail
    # 3 - пароли не совпадают

    if current_user.access < 5:
        return abort(403)

    form = AdminRegisterForm()

    # форма заполнена относительно-корректно
    if form.validate_on_submit():
        # print(form.data)
        # print(form.login.data)
        # print(form.email.data)
        # print(form.name.data)
        # print(form.occupation.data)
        # print(form.access.data)
        # print(form.password.data)
        # print(form.repeat_password.data)

        db_sess = db_session.create_session()  # создаём сессию
        user = db_sess.query(User).filter(User.login == form.login.data.strip()).first()

        # Пользователь не существует - это хорошо
        if not user:
            if form.password.data == form.repeat_password.data:
                # Регистрируем пользователя
                user = User()
                chat = Chat()

                chat.title = "Сохранённые сообщения"

                user.name = form.name.data
                user.login = form.login.data
                if form.email.data and verify_email(form.email.data):
                    user.email = form.email.data
                user.occupation = form.occupation.data
                user.access = int(form.access.data)
                user.hashed_password = generate_password_hash(form.password.data)
                user.chats.append(chat)

                db_sess.add(user)
                db_sess.commit()

                return redirect('/')
            else:
                # Пароли не совпадают - ошибка
                return render_template("admin/register.html", title="Регистрация", form=form, error=3,
                                       message="Пароли не совпадают!")
        else:
            # Пользователь уже существует - ошибка
            return render_template("admin/register.html", title="Регистрация", form=form, error=1,
                                   message="Пользователь уже существует!")
    # Первый вход, никаких данных
    return render_template("admin/register.html", title="Регистрация", form=form, error=0)


# Чаты
@app.route("/write/")
@login_required
def write():
    """Страница создания/открытия чата с выбранным пользователем"""
    parameters = request.args
    if "user" in parameters:
        try:
            user = int(parameters["user"])
            if user == current_user.id:
                return redirect("/400")
            db = db_session.create_session()
            user = db.query(User).filter(User.id == user).first()

            if user is not None and user.access <= current_user.access:
                for chat in user.chats:
                    if len(chat.users) == 2 and (chat.users[0].id == current_user.id or
                                                 chat.users[1].id == current_user.id):
                        return redirect(f"/chat/{chat.id}")

                chat = Chat()
                chat.title = current_user.name + " & " + user.name
                chat.users.append(user)
                user = db.query(User).filter(User.id == current_user.id).first()
                chat.users.append(user)

                db.commit()

                return redirect(f"/chat/{chat.id}")
            elif user is None:
                return redirect("/404")
            return redirect("/400")
        except Exception:
            return redirect("/400")
    elif "login" in parameters:
        db = db_session.create_session()
        user = db.query(User).filter(User.login == parameters["login"]).first()

        if user is not None:
            return redirect(f"/write?user={user.id}")
        return redirect(f"/write?user={parameters['login']}")
    else:
        return redirect("/400")


@app.route("/user/chat/")
@app.route("/chat/")
@login_required
def chats():
    """Страница чатов текущего пользователя"""
    return render_template("chat.html", title="Чаты")


@app.route("/user/chat/<int:chat_id>")
@app.route("/chat/<int:chat_id>")
@login_required
def chat(chat_id: int):
    """Страница конкретного чата"""
    chat = list(filter(lambda chat: chat.id == chat_id, current_user.chats))

    if chat:
        return render_template("chat.html", title=f"Чат \"{chat[0].title}\"", chat=chat[0])
    return abort(404)


# Статьи
@app.route("/articles/find/<find>")
@app.route("/articles")
@login_required
def find_articles(find=""):
    """Страница поиска статей"""

    db_sess = db_session.create_session()

    # Поиск необходим - что-то есть в поле ввода
    if find:
        # Ищем статьи по запросу
        articles = db_sess.query(Article).filter(Article.access <= current_user.access).all()
        articles = list(filter(lambda article: find.lower() in article.title.lower(), articles))
        return render_template("articles.html", title=f"Результаты поиска по запросу {repr(find)}",
                               articles=articles, now=datetime.datetime.now(), find=find)

    # Показываем все статьи
    articles = db_sess.query(Article).filter(Article.access <= current_user.access).all()
    return render_template("articles.html", title="Статьи", articles=articles,
                           now=datetime.datetime.now())


@app.route("/article/<article>")
@login_required
def get_article(article):
    """Страница со статьёй"""
    # Ищем статью
    db_sess = db_session.create_session()
    article_ = db_sess.query(Article).filter(Article.link == article).first()

    if article_:
        if current_user.access < article_.access:
            return abort(403, article_.access)
        return render_template(f"articles/{article}.html", title=f"Статья {repr(article_.title)}")
    # Статья не найдена
    return abort(404, "Статья не найдена")


@app.route("/article/add", methods=["GET", "POST"])
@app.route("/user/article/add", methods=["GET", "POST"])
@login_required
def add_article():
    """Страница добавления статьи"""
    form = ArticleAddForm()

    if form.validate_on_submit():
        db = db_session.create_session()
        article = db.query(Article).filter(Article.link == form.link.data).first()

        if article is None:
            form.file.data.save(os.path.join(f"templates/articles/", form.link.data + ".html"))

            article = Article()
            article.title = form.title.data
            article.about = form.description.data
            article.link = form.link.data
            article.access = current_user.access

            user = db.query(User).filter(User.id == current_user.id).first()
            user.articles.append(article)

            db.commit()

            return redirect("/user/articles/")

    return render_template("add_article.html", title="Добавление статьи", form=form)


@app.route("/user/articles/")
@login_required
def personal_articles():
    """Статьи текущего пользователя"""
    parameters = request.args

    if "user" in parameters and parameters["user"].isdigit():
        db = db_session.create_session()
        user = db.query(User).filter(User.id == int(parameters["user"])).first()
        if user:
            articles = user.articles
        else:
            articles = current_user.articles
    else:
        articles = current_user.articles  # получаем статьи

    return render_template("articles.html", title="Ваши статьи", articles=articles,
                           now=datetime.datetime.now())


@app.route("/user/article/<article>/delete")
@app.route("/article/<article>/delete")
@login_required
def delete_article(article):
    db = db_session.create_session()

    article = db.query(Article).filter(
        (Article.link == article) & (Article.owner == current_user.id)).first()

    if article:
        os.remove(os.path.join("templates/articles/", article.link + ".html"))

        db.delete(article)
        db.commit()

        return redirect("/articles")
    return abort(404)


@app.route("/user/settings/", methods=["GET", "POST"])
@app.route("/settings/", methods=["GET", "POST"])
@login_required
def settings():
    """Страница настроек"""

    form = SettingsForm()

    if form.validate_on_submit():
        db_sess = db_session.create_session()

        # Логин верен
        if (current_user.login != form.login.data and db_sess.query(User).filter(
                User.login == form.login.data).first() is None) or current_user.login == \
                form.login.data:
            user = db_sess.query(User).filter(User.login == form.login.data).first()
            print(user)
            if form.email.data and verify_email(form.email.data):
                if form.image.data.filename and form.image.data.content_type.startswith("image/"):
                    filename = secure_filename(form.image.data.filename)
                    form.image.data.save(os.path.join("static/images/users/", filename))

                    user.login = form.login.data
                    user.name = form.name.data
                    if form.password.data:
                        user.hashed_password = generate_password_hash(form.password.data)
                    user.image = filename

                    db_sess.commit()
                else:
                    user.login = form.login.data
                    user.name = form.name.data
                    if form.password.data:
                        user.hashed_password = generate_password_hash(form.password.data)

                    db_sess.commit()
            else:
                user = db_sess.query(User).filter(User.login == current_user.login).first()

                if form.image.data.filename and form.image.data.content_type.startswith("image/"):
                    filename = secure_filename(form.image.data.filename)
                    form.image.data.save(os.path.join("static/images/users/", filename))

                    user.login = form.login.data
                    user.name = form.name.data
                    if form.password.data:
                        user.hashed_password = generate_password_hash(form.password.data)
                    user.image = filename

                    db_sess.commit()
                else:
                    user.login = form.login.data
                    user.name = form.name.data
                    if form.password.data:
                        user.hashed_password = generate_password_hash(form.password.data)

                    db_sess.commit()
        return render_template("settings.html", title="Настройки", form=form, error=0)

    form.login.data = current_user.login
    form.email.data = current_user.email
    form.name.data = current_user.name

    return render_template("settings.html", title="Настройки", form=form, error=0)


@app.route("/")
@app.route("/index/")
@app.route("/user/")
@login_required
def index():
    """Главная страница пользователя"""
    db = db_session.create_session()
    parameters = request.args
    if "user" in parameters:
        if parameters["user"].isdigit() and int(parameters["user"]) != current_user.id:

            user = db.query(User).filter(User.id == int(parameters["user"])).first()

            if user:
                if user.access <= current_user.access:
                    number_of_videos = (len(db.query(Video).filter(Video.owner == user.id).all()))
                    return render_template("user.html", title=f"Страница пользователя {user.name}",
                                           number_of_videos=number_of_videos,
                                           user=user)
                return abort(403)
            return abort(404, "Пользователь не найден!")
        elif parameters["user"].isdigit():
            return redirect("/user")
    number_of_videos = (len(db.query(Video).filter(Video.owner == current_user.id).all()))

    return render_template("index.html", title="Ваш профиль", number_of_videos=number_of_videos)


@app.route("/favicon.ico")
def icon():
    """Иконка сайта"""
    return redirect("/static/images/icon.svg")


if __name__ == '__main__':
    db_session.global_init("data/db/database.db")

    app.run()
