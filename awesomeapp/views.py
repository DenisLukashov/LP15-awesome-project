from awesomeapp import app, db
from .forms import LoginForm
from .models import User

from flask_login import current_user, login_user
from flask import render_template, request, flash, redirect, url_for
from werkzeug.urls import url_parse

@app.route('/')
def index():
    return 'Hello'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if User is not None and user.check_password(form.password.data):
            login_user(user, remember_me=form.remember_me.data)
            desired_page = request.args.get('next')
            if not desired_page or url_parse(desired_page).netloc != '':
                return redirect(url_for('index'))
            return redirect(desired_page)
        flash('Не верный email или пароль')
        return redirect(url_for('login'))
    form = LoginForm()
    return render_template('login.html', form=form)