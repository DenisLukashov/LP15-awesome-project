from awesomeapp.extensions import db

class Stats(db.Model):
    __tablename__ = 'stats'
    id = db.Column(db.Integer, primary_key=True)

    equipment_id = db.Column(
		db.Integer,
		db.ForeignKey('equipment.id', ondelete='CASCADE'),
		index=True
    )
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

    story_id = db.Column(
    	db.Integer,
    	db.ForeignKey('stories.id', ondelete='CASCADE'),
    	index=True
    )
    story = db.relationship('Story', uselist=False, 
                        backref='stats', foreign_keys='Story.stats_id')


class Story(db.Model):
    __tablename__ = 'stories'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
 
    stats_id = db.Column(
    	db.Integer, 
    	db.ForeignKey('stats.id', ondelete='CASCADE'), 
    	index=True
    )
    
    
class Image(db.Model):
    __tablename__ = 'images'
    id = db.Column(db.Integer, primary_key=True)
    src = db.Column(db.Text)
    
    story_id = db.Column(
    	db.Integer,
		db.ForeignKey('stories.id', ondelete='CASCADE'), 
		index=True
    )
    story = db.relationship('Story', backref='images') 
