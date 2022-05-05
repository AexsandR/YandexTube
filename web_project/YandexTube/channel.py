from flask import Flask, render_template, redirect, request, abort, url_for, flash
from data import db_session
import flask
from data.__all_models import *  # импорт всех orm-моделей
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

blueprint = flask.Blueprint(
    'channel',
    __name__,
    template_folder='templates'
)


@blueprint.route("/channel/<int:id>")
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
        return render_template("channel.html", logo_channel=url_for('static', filename=f"images/users/{channel.image}"),
                               channel=channel, time=channel.created_date, data=videos)
