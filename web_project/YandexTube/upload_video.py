import flask
from flask import Flask, render_template, redirect, request, abort, url_for, flash
from data import db_session
from data.__all_models import *  # импорт всех orm-моделей
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from werkzeug.utils import secure_filename

from YandexTube.setting_img import setting_image
from data.forms import uploud


blueprint = flask.Blueprint(
    'upload_video',
    __name__,
    template_folder='templates'
)

@blueprint.route('/upload_video', methods=['GET', 'POST'])
def video():
    form = uploud.Uploud_forms()
    if form.validate_on_submit():
        photo_user = form.photo_user.data
        video_user = form.video_user.data
        video_user_filename = secure_filename(video_user.filename)
        photo_user_filename = secure_filename(photo_user.filename)
        if '.mp4' in video_user_filename and ".png" in photo_user_filename:
            video = Video()
            video.name = form.name.data
            video.owner = current_user.id
            db = db_session.create_session()
            db.add(video)
            db.commit()
            id = video.id
            video_user.save('./static/video/' + f"{id}.mp4")
            photo_user.save('./static/video/poster/' + f"{id}.png")
            setting_image('./static/video/poster/' + f"{id}.png")
            return redirect('/YandexTube')
    return render_template("add_video.html", form=form)
