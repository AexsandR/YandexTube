import flask
from flask import Flask, render_template, redirect, request, abort, url_for, flash
from data import db_session
from data.__all_models import *  # импорт всех orm-моделей

blueprint = flask.Blueprint(
    'main_page_YandexTube',
    __name__,
    template_folder='templates'
)


@blueprint.route('/YandexTube', methods=['GET', 'POST'])
def home():
    db_sess = db_session.create_session()
    data = db_sess.query(Video).all()
    for i in data:
        if len(i.name) > 25:
            i.name = i.name[:25] + '...'
    return render_template("pass.html", data=data[::-1])
