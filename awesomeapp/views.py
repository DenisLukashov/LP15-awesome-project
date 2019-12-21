from flask_login import current_user, login_user, logout_user
from flask import render_template, request, flash, redirect, url_for
from werkzeug.urls import url_parse

from config import Config
from awesomeapp import app, db, login, send_from_directory
from .forms import LoginForm
from .models import User




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
    
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


# @app.route('/<path>/<filename>')
# def send_static(path,filename):
#     return send_from_directory(f'{Config.STATIC_FOLDER}/{path}', filename)