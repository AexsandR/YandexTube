import flask
from flask import Flask, render_template, redirect, request, abort, url_for, flash
from data import db_session
from data.__all_models import *  # импорт всех orm-моделей
from fuzzywuzzy import fuzz

blueprint = flask.Blueprint(
    'search',
    __name__,
    template_folder='templates'
)

@blueprint.route('/search/<answer>', methods=['GET', 'POST'])
def search(answer):
    answer = answer.split('_')
    answer = ' '.join(answer)
    answer_channels = []
    answer_videos = []
    db_sess = db_session.create_session()
    channels = db_sess.query(User).all()
    videos = db_sess.query(Video).all()
    for channel in channels:
        if answer.lower() in channel.name.lower() or fuzz.partial_ratio(channel.name, answer) >= 75:
            answer_channels.append(channel)
    for video in videos:
        if answer.lower() in video.name.lower() or fuzz.partial_ratio(video.name, answer) >= 75:
            answer_videos.append([video.id, url_for('static', filename=f'video/poster/{video.id}.png'), video.name])
    return render_template("search.html", channels=answer_channels, data=answer_videos)