import flask
from flask import Flask, render_template, redirect, request, abort, url_for, flash
from data import db_session
from data.__all_models import *  # импорт всех orm-моделей
from data.forms import video_form
from flask_login import current_user

blueprint = flask.Blueprint(
    'watch_video',
    __name__,
    template_folder='templates'
)


@blueprint.route('/watch_video/<int:id>', methods=['GET', 'POST'])
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
        return redirect(f'/watch_video/{id}')
    if current_user.is_authenticated:
        check = db_sess.query(Subscriptions).filter(
            Subscriptions.who_subscribed == current_user.id,
            Subscriptions.who_did_you_subscribe_to == channel.id).first()
        if check:
            status_sub = False
        else:
            status_sub = True
    else:
        status_sub = False
    return render_template("video.html", path=url_for('static', filename=f"video/{video.id}.mp4"), videos=videos,
                           video=video, channel=channel, form=form,
                           logo_channel=url_for('static', filename=f"images/users/{channel.image}"), status_sub=status_sub,
                           comments=temp)
