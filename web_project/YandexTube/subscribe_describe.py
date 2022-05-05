from flask import Flask, render_template, redirect, request, abort, url_for, flash
from data import db_session
import flask
from data.__all_models import *  # импорт всех orm-моделей
from flask_login import LoginManager, login_user, logout_user, login_required, current_user



blueprint = flask.Blueprint(
    'subscribe_describe',
    __name__,
    template_folder='templates'
)


@blueprint.route('/subscribe/<int:id>')
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
    return redirect(f"/watch_video/{id}")


@blueprint.route("/describe/<int:id>")
def describe(id):
    try:
        db_sess = db_session.create_session()
        video = db_sess.query(Video).filter(Video.id == id).first()
        channel = db_sess.query(User).filter(User.id == video.owner).first()
        subscription = db_sess.query(Subscriptions).filter(
            Subscriptions.who_subscribed == current_user.id, Subscriptions.who_did_you_subscribe_to == channel.id).first()
        db_sess.delete(subscription)
        channel.folowers -= 1
        db_sess.add(channel)
        db_sess.commit()
    except Exception:
        return redirect(f"/watch_video/{id}")
    else:
        return redirect(f"/watch_video/{id}")