import imghdr
import os

from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user

from awesomeapp.extensions import db
from config import Config
from awesomeapp.user.models import User
from awesomeapp.user.forms import RegistrationForm, LoginForm
from awesomeapp.utils import get_redirect_target

blueprint = Blueprint(
    'user',
    __name__,
    url_prefix='/users',
    template_folder='templates'
)


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('vizit.start_page'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(get_redirect_target())
        flash('Не верный email или пароль')
        return redirect(url_for('.login'))
    return render_template('user/login.html', title='Вход', form=form)


@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('user.visit'))


@blueprint.route('/visit')
def visit():
    src = [
        os.path.join(Config.EQUIPMENT_ICON_PATH, x)
        for x in Config.STOCK_ICON.values()
    ]
    return render_template(
        'user/visit.html',
        title='Привет, спортсмен!',
        src=src)


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('equipment.equipment'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            first_name=form.first_name.data or None,
            second_name=form.second_name.data or None,
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
            avatar.save(os.path.join(
                Config.GLOBAL_PATH,
                Config.IMAGE_PATH,
                filename))
            user.avatar = os.path.join(Config.IMAGE_PATH, filename)
            db.session.add(user)
            db.session.commit()
        return redirect(url_for('.login'))
    return render_template(
        'user/register.html',
        title='Регистрация',
        form=form
    )
