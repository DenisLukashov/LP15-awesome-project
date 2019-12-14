from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30))
    second_name = db.Column(db.String(30))
    email = db.Column(db.String(40), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.Text)
    avatar = db.Column(db.String(100))
    equipment = db.relationship('Equipment', backref='user')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    
class Story(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    story_text = db.Column(db.Text)
    
    images = db.relationship('Image', backref='story')
    
    stats_id = db.Column(db.Integer, db.ForeignKey('stats.id'))
    stats = db.relationship('Stats', backref='story')
    
    
class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    src = db.Columnm(db.Text)
    story_id = db.Column(db.Integer, db.ForeignKey('story.id'))
        
