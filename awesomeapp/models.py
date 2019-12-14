from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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
