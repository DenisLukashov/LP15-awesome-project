from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Equipment(db.Model):
    __tablename__ = 'equipment'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String, nullable=False, unique=False)
    e_type = db.Column(db.SmallInteger, nullable=False, unique=False)  
    avatar = db.Column(db.String, nullable=True, unique=False)
    about = db.Column(db.Text, nullable=True, unique=False)
    stats = db.relationship("Stats")


class Stats(db.Model):
    __tablename__ = 'stats'
    id = db.Column(db.Integer, primary_key=True)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'))
    date = db.Column(db.Date, nullable=False, unique=False)
    distance = db.Column(db.BigInteger, nullable=True, unique=False)
    time = db.Column(db.BigInteger, nullable=True, unique=False)
    total_time = db.Column(db.BigInteger, nullable=True, unique=False)
    max_speed = db.Column(db.BigInteger, nullable=True, unique=False)
    steps = db.Column(db.BIgInteger, nullable=True, unique=False)
    avg_cadence = db.Column(db.SmallInteger, nullable=True, unique=False)
    max_cadence = db.Column(db.SmallInteger, nullable=True, unique=False)
    avg_heart_rate = db.Column(db.SmallInteger, nullable=True, unique=False)
    max_heart_rate = db.Column(db.SmallInteger, nullable=True, unique=False)
    max_temperature = db.Column(db.Float, nullable=True, unique=False)
    min_temperature = db.Column(db.Float, nullable=True, unique=False)
    start_altitude = db.Column(db.SmallInteger, nullable=True, unique=False)
    total_up_altitude = db.Column(db.SmallInteger, nullable=True, unique=False)
    total_down_altitude = db.Column(db.SmallInteger, nullable=True, unique=False)
    min_altitude = db.Column(db.SmallInteger, nullable=True, unique=False)
    max_altitude = db.Column(db.SmallInteger, nullable=True, unique=False)
    story_id = db.relationship("Story", uselist=False, back_populates="stats")
