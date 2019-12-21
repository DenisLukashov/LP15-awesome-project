import imghdr
import os

from flask import render_template, redirect, url_for, send_from_directory
from flask_login import current_user

from awesomeapp import app, db, login
from config import Config
from .models import User
from .forms import RegistrationForm


@app.route('/')
def index():
    return 'Hello world!'

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            first_name=form.first_name.data,
            second_name=form.second_name.data,
            email=form.email.data,
            about_me=form.about_me.data,
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        avatar = form.avatar.data
        if avatar:
            file_type = imghdr.what(avatar)
            filename = f'{user.id}.{file_type}'
            avatar.save(os.path.join(Config.GLOBAL_IMAGE_PATH, filename))
            user.avatar = os.path.join(Config.IMAGE_PATH, filename)
            db.session.add(user)
            db.session.commit()
        return redirect(url_for('index'))
    return render_template('register.html', title='Регистрация', form=form)
    
@app.route('/static/<path>/<filename>')
def send_static(path, filename):
    return send_from_directory(f'{Config.STATIC_FOLDER}/{path}', filename)
