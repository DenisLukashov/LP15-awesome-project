from awesomeapp import app, db, login
from .models import User
from .forms import RegistrationForm
from config import Config
from flask import render_template, redirect, url_for
from flask_login import current_user
import imghdr
import os


@app.route('/')
def index():
    return 'Hello'

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
            about=form.about.data,
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        avatar = form.avatar.data
        if avatar:
            user = User.query.filter_by(email=form.email.data)
            filename = f'{user.id}.{imghdr.what(avatar)}'
            avatar.save(os.path.join(Config.STATIC_IMAGE_PATH, filename))
            user = User(
                avatar = f'{Config.STATIC_IMAGE_PATH}/{filename}'
            )
            db.session.add(user)
            db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
