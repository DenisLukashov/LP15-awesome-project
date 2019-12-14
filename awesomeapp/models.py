from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'user'
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


class Equipment(db.Model):
    __tablename__ = 'equipment'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String, nullable=False)
    type = db.Column(db.SmallInteger, nullable=False)  
    avatar = db.Column(db.String)
    about = db.Column(db.Text)
    stats = db.relationship("Stats", backref='equipment')


class Stats(db.Model):
    __tablename__ = 'stats'
    id = db.Column(db.Integer, primary_key=True)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'))
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
    story_id = db.Column(db.Integer, db.ForeignKey('story.id'))
    story = db.relationship("Story", uselist=False, back_populates="stats")
  
    
class Story(db.Model):
    __tablename__ = 'story'
    id = db.Column(db.Integer, primary_key=True)
    story_text = db.Column(db.Text)
    
    images = db.relationship('Image', backref='story')
    
    stats_id = db.Column(db.Integer, db.ForeignKey('stats.id'))
    stats = db.relationship('Stats', backref='story')
    
    
class Image(db.Model):
    __tablename__ = 'image'
    id = db.Column(db.Integer, primary_key=True)
    src = db.Columnm(db.Text)
    story_id = db.Column(db.Integer, db.ForeignKey('story.id'))
