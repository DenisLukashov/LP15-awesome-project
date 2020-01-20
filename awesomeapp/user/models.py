import os

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)
from flask_login import UserMixin

from config import Config
from awesomeapp.extensions import db


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), default='Я не заполнил имя')
    second_name = db.Column(db.String(64), default='Я не заполнил фамилию')
    email = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.Text)
    avatar = db.Column(
        db.String(128),
        default=os.path.join(Config.IMAGE_PATH, 'default-avatar.png')
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
