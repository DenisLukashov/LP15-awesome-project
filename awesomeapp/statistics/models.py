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
    story = db.relationship(
        'Story', uselist=False,
        backref='stats',
        foreign_keys='Story.stats_id'
    )

    @classmethod
    def filter_by_date_and_equipment(cls, function, id, start_date, end_date):
        query = db.session.query(db.func.coalesce(
            function, 0)
        ).filter(
            cls.equipment_id == id
        ).filter(
            start_date <= cls.date
        ).filter(
            cls.date <= end_date
        ).scalar()
        return query

    @classmethod
    def stats_filter_by_date(cls, id, start_date, end_date):
        query = cls.query.filter(
            cls.equipment_id == id
        ).filter(
            start_date <= cls.date
        ).filter(
            cls.date <= end_date
        ).order_by(
            cls.date
        ).all()
        return query

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
