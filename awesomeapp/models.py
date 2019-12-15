from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64))
    second_name = db.Column(db.String(64))
    email = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.Text)
    avatar = db.Column(db.String(128))
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Equipment(db.Model):
    __tablename__ = 'equipment'
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref='equipment')

    name = db.Column(db.String(128), nullable=False)
    type = db.Column(db.SmallInteger, nullable=False)  
    avatar = db.Column(db.String(128))
    about = db.Column(db.Text)


class Stats(db.Model):
    __tablename__ = 'stats'
    id = db.Column(db.Integer, primary_key=True)

    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'))
    equipment = db.relationship('Equipment', backref='stats')

    date = db.Column(db.Date, nullable=False)
    distance = db.Column(db.BigInteger)
    time = db.Column(db.BigInteger)
    total_time = db.Column(db.BigInteger)
    max_speed = db.Column(db.BigInteger)
    steps = db.Column(db.BigInteger)
    avg_cadence = db.Column(db.SmallInteger)
    max_cadence = db.Column(db.SmallInteger)
    avg_heart_rate = db.Column(db.SmallInteger)
    max_heart_rate = db.Column(db.SmallInteger)
    max_temperature = db.Column(db.Float)
    min_temperature = db.Column(db.Float)
    start_altitude = db.Column(db.SmallInteger)
    total_up_altitude = db.Column(db.SmallInteger)
    total_down_altitude = db.Column(db.SmallInteger)
    min_altitude = db.Column(db.SmallInteger)
    max_altitude = db.Column(db.SmallInteger)
    
    story_id = db.Column(db.Integer, db.ForeignKey('stories.id'))
    story = db.relationship('Story', uselist=False, backref='stats')
  
    
class Story(db.Model):
    __tablename__ = 'stories'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
 
    stats_id = db.Column(db.Integer, db.ForeignKey('stats.id'))
    
    
class Image(db.Model):
    __tablename__ = 'images'
    id = db.Column(db.Integer, primary_key=True)
    src = db.Column(db.Text)
    
    story_id = db.Column(db.Integer, db.ForeignKey('stories.id'))
    story = db.relationship('Story', backref='images') 
