
import imghdr
import os

from flask import render_template, redirect, url_for, send_from_directory, request, flash
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse

from awesomeapp import app, db, login
from config import Config
from .models import User, Stats, Story, Image
from .forms import RegistrationForm, LoginForm, Statistics


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            desired_page = request.args.get('next')
            if not desired_page or url_parse(desired_page).netloc != '':
                return redirect(url_for('index'))
            return redirect(desired_page)
        flash('Не верный email или пароль')
        return redirect(url_for('login'))
    
    return render_template('login.html', title='Войти', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


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
            avatar.save(os.path.join(Config.GLOBAL_PATH, Config.IMAGE_PATH, filename))
            user.avatar = os.path.join(Config.IMAGE_PATH, filename)
            db.session.add(user)
            db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', title='Регистрация', form=form)

@app.route('/stats', methods=['GET', 'POST'])
def set_stats():
    form = Statistics()
    if form.validate_on_submit():
        story = Story(
            text = form.story.data
        )
        stats = Stats(
            date = form.date.data,
            distance = convert_to_meter(form.distance.data),
            time = convert_to_seconds(form.time.data),
            total_time = convert_to_seconds(form.total_time.data),
            max_speed = convert_to_meter(form.max_speed.data),
            steps = form.steps.data,
            avg_cadence = form.avg_cadence.data,
            max_cadence = form.max_cadence.data,
            avg_heart_rate = form.avg_heart_rate.data,
            max_heart_rate = form.max_heart_rate.data,
            max_temperature = form.max_temperature.data,
            min_temperature = form.min_temperature.data,
            start_altitude = form.start_altitude.data,
            total_up_altitude = form.total_up_altitude.data,
            total_down_altitude = form.total_down_altitude.data,
            min_altitude = form.min_altitude.data,
            max_altitude = form.max_altitude.data,
        )
        db.session.add(story)
        db.session.commit()
        db.session.add(stats)
        db.session.commit()
        images = form.photoes.data
        if str(images[0]).find('application/octet-stream') == -1:
            for image in images:
                img = Image()
                db.session.add(img)
                db.session.commit()
                file_type = imghdr.what(image)
                filename = f'{img.id}.{file_type}'
                image.save(os.path.join(Config.GLOBAL_PATH, Config.STORY_IMAGE_PATH, filename))
                img.src = os.path.join(Config.STORY_IMAGE_PATH, filename)
                db.session.add(img)
                db.session.commit()
    return render_template('stats.html', title='Ввод данных', form=form)

def convert_to_seconds(time):
    if not time:
        return None
    unit_of_time = [int(x) for x in time.split(':')]
    coefficient = [3600, 60 , 1]
    return sum(x * y for x, y in zip(unit_of_time, coefficient))

def convert_to_meter(value):
    if value is None:
        return None
    return value*1000

@app.route('/static/<path>/<filename>')
def send_static(path, filename):
    return send_from_directory(f'{Config.STATIC_FOLDER}/{path}', filename)
