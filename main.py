from flask import Flask, render_template, redirect, request, abort, url_for, flash
from data import db_session
from forms import login_form
from data.__all_models import *  # импорт всех orm-моделей
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from forms import reg_forms
from werkzeug.utils import secure_filename
from forms import video_form
from test import setting_image
from forms import uploud
import os
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)
db_session.global_init("db/blogs.db")

@app.before_request
def search():
    if request.method == 'POST':
        if 'search' in request.form:
            print(request.form['search'])
        print('ok')


@app.route('/', methods=['GET', 'POST'])
def home():
    db_sess = db_session.create_session()

    data = db_sess.query(Video).all()
    for i in data:
        if len(i.name) > 25:
            i.name = i.name[:25] + '...'
    try:
        return render_template("pass.html", data=data[::-1], photo=url_for('static', filename=f"{current_user.image}"))
    except Exception:
        return render_template("pass.html", data=data[::-1])



@app.route('/watch_video/id=<int:id>', methods=['GET', 'POST'])
def watch_video(id):
    form = video_form.Video_form()
    db_sess = db_session.create_session()
    video = db_sess.query(Video).filter(Video.id == id).first()
    comments = db_sess.query(Comment).filter(Comment.video_id == id).all()[::-1]
    temp = []
    for i in comments:
        user = db_sess.query(User).filter(User.id == i.owner).first()
        temp.append([user, i])
    videos = db_sess.query(Video).all()
    video.views += 1
    db_sess.commit()
    channel = db_sess.query(User).filter(User.id == video.owner).first()
    if form.validate_on_submit():
        comment = Comment()
        comment.owner = current_user.id
        comment.video_id = id
        comment.text = form.comment.data
        db_sess.add(comment)
        db_sess.commit()
        return redirect(f'/watch_video/id={id}')
    try:
        check = db_sess.query(Subscriptions).filter(
            Subscriptions.who_subscribed == current_user.id,
            Subscriptions.who_did_you_subscribe_to == channel.id).first()
        print(check)
        print(channel.id)
        if check:
            status_sub = False
        else:
            status_sub = True

        return render_template("video.html", path=url_for('static', filename=f"video/{video.id}.mp4"),
                               photo=url_for('static', filename=f"{current_user.image}"), videos=videos,
                               video=video, channel=channel, form=form,
                               logo_channel=url_for('static', filename=f"{channel.image}"), status_sub=status_sub,
                               comments=temp)
    except Exception:
        return render_template("video.html", path=url_for('static', filename=f"video/{video.id}.mp4"),
                               channel=channel, videos=videos, form=form,
                               video=video, logo_channel=url_for('static', filename=f"{channel.image}"),
                               status_sub=False, comments=temp)


@app.route('/upload_video', methods=['GET', 'POST'])
def video():
    form = uploud.Uploud_forms()
    if form.validate_on_submit():
        file = form.file.data
        file1 = form.file1.data
        filename = secure_filename(file1.filename)
        filename1 = secure_filename(file.filename)
        print(type(filename), filename)
        print(type(filename1), filename1)
        if '.mp4' in filename and ".png" in filename1:
            video = Video()
            video.name = form.name.data
            video.owner = current_user.id
            db = db_session.create_session()
            db.add(video)
            db.commit()
            id = video.id
            file1.save('./static/video/' + f"{id}.mp4")
            file.save('./static/video/poster/' + f"{id}.png")
            setting_image('./static/video/poster/' + f"{id}.png")
            print('ok')
            return redirect('/')
    return render_template("add_video.html", form=form, photo=url_for('static', filename=f"{current_user.image}"))


@app.route('/login/reg', methods=['GET', 'POST'])
def reg():
    form = reg_forms.RegForm()
    if form.validate_on_submit():
        if form.Reapeat_password.data == form.password.data:
            db_session.global_init("db/blogs.db")
            user = User()
            user.set_password(form.password.data)
            user.name = form.name.data
            user.email = form.email.data
            db_sess = db_session.create_session()
            db_sess.add(user)
            db_sess.commit()
            user = db_sess.query(User).filter(User.email == form.email.data).first()
            login_user(user, remember=True)
            return redirect('/')
    return render_template("reg.html", title='регистрация', form=form)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = login_form.LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='войти', form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/subscribe&id=<int:id>')
def subscribe(id):
    db_sess = db_session.create_session()
    video = db_sess.query(Video).filter(Video.id == id).first()
    channel = db_sess.query(User).filter(User.id == video.owner).first()
    check = db_sess.query(Subscriptions).filter(
        Subscriptions.who_subscribed == current_user.id, Subscriptions.who_did_you_subscribe_to == channel.id).first()
    if check or channel.id == current_user.id:
        return redirect(f"/watch_video/id={id}")
    subscriptions = Subscriptions()
    subscriptions.who_subscribed = current_user.id
    subscriptions.who_did_you_subscribe_to = channel.id
    channel.folowers += 1
    db_sess.add(subscriptions)
    db_sess.add(channel)
    db_sess.commit()
    return redirect(f"/watch_video/id={id}")


@app.route("/describe&id=<int:id>")
def describe(id):
    db_sess = db_session.create_session()
    video = db_sess.query(Video).filter(Video.id == id).first()
    channel = db_sess.query(User).filter(User.id == video.owner).first()
    check = db_sess.query(Subscriptions).filter(
        Subscriptions.who_subscribed == current_user.id, Subscriptions.who_did_you_subscribe_to == channel.id).first()
    print(check.who_subscribed, check.who_did_you_subscribe_to)
    db_sess.delete(check)
    channel.folowers -= 1
    db_sess.add(channel)
    db_sess.commit()
    return redirect(f"/watch_video/id={id}")


@app.route("/channel&id=<int:id>")
def channel(id):
    db_sess = db_session.create_session()
    videos = db_sess.query(Video).filter(Video.owner == id).all()
    channel = db_sess.query(User).filter(User.id == id).first()
    for i in videos:
        if len(i.name) > 25:
            i.name = i.name[:25] + '...'
    if current_user.is_authenticated and current_user.id == id:
        if videos:
            video = max(videos, key=lambda x: x.views)
        else:
            video = False
        return render_template("my_channel.html", video=video, folowers=channel.folowers,
                               photo=url_for('static', filename=f"{current_user.image}"), time=channel.created_date,
                               data=videos)
    else:
        return render_template("channel.html", logo_channel=url_for('static', filename=f"{channel.image}"),
                               channel=channel, photo=url_for('static', filename=f"{current_user.image}"),
                               time=channel.created_date, data=videos)


@app.route('/subscriptions')
def subscriptions():
    db_sess = db_session.create_session()
    channels_id = db_sess.query(Subscriptions).filter(Subscriptions.who_subscribed == current_user.id)
    channels = []
    for i in channels_id:
        channel = db_sess.query(User).filter(User.id == i.who_did_you_subscribe_to).first()
        channels.append(channel)
    data = []
    for i in channels_id:
        video = db_sess.query(Video).filter(Video.owner == i.who_did_you_subscribe_to).first()
        data.append(video)
    for i in data:
        if len(i.name) > 25:
            i.name = i.name[:25] + '...'
    data = data[::-1]
    return render_template("subscriptions.html", channels=channels * 10, data=data * 100,
                           photo=url_for('static', filename=f"{current_user.image}"))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)