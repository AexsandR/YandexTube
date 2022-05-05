from flask import Flask, render_template, redirect, request, abort, url_for, flash
from data import db_session
import flask
from data.__all_models import *  # импорт всех orm-моделей
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

blueprint = flask.Blueprint(
    'subscriptions',
    __name__,
    template_folder='templates'
)


@blueprint.route('/subscriptions')
def subscriptions():
    db_sess = db_session.create_session()
    channels_id = db_sess.query(Subscriptions).filter(Subscriptions.who_subscribed == current_user.id)
    channels = []
    for i in channels_id:
        channel = db_sess.query(User).filter(User.id == i.who_did_you_subscribe_to).first()
        channels.append(channel)
    data = []
    for i in channels_id:
        videos = db_sess.query(Video).filter(Video.owner == i.who_did_you_subscribe_to).all()
        for video in videos:
            data.append(video)
    for i in data:
        if len(i.name) > 25:
            i.name = i.name[:25] + '...'
    data = sorted(data, key=lambda x: x.id)
    data = data[::-1]
    return render_template("subscriptions.html", channels=channels, data=data)
