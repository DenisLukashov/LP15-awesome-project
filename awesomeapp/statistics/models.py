from datetime import timedelta

from awesomeapp.extensions import db

from config import Config
from awesomeapp.statistics.utils import convert_time_to_user_view


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

    @classmethod
    def get_statistics(cls, id, start_date, end_date):
        statistics = {

            'Тренировок': cls.query.filter(
                cls.equipment_id == id
            ).filter(
                start_date <= cls.date
            ).filter(
                cls.date <= end_date
            ).count(),

            'Дистанция': cls.filter_by_date_and_equipment(
                db.func.sum(
                    cls.distance), id, start_date, end_date
                ) / Config.METERS_PER_KILOMETER,

            'Время упражнения': convert_time_to_user_view(
                cls.filter_by_date_and_equipment(
                    db.func.sum(
                        cls.time), id, start_date, end_date
                )
            ),

            'Общее время тренировки': convert_time_to_user_view(
                cls.filter_by_date_and_equipment(
                    db.func.sum(
                        cls.total_time), id, start_date, end_date
                )
            ),

            'Всего шагов': cls.filter_by_date_and_equipment(
                db.func.sum(
                    cls.steps), id, start_date, end_date
            ),

            'Подъем':  cls.filter_by_date_and_equipment(
                db.func.sum(
                    cls.total_up_altitude), id, start_date, end_date
            ),

            'Спуск': cls.filter_by_date_and_equipment(
                db.func.sum(
                    cls.total_down_altitude), id, start_date, end_date
            ),

            'Макс. скорость': cls.filter_by_date_and_equipment(
                db.func.max(
                    cls.max_speed), id, start_date, end_date
            ) / Config.METERS_PER_KILOMETER,

            'Макс. каденс': cls.filter_by_date_and_equipment(
                db.func.max(
                    cls.max_cadence), id, start_date, end_date
            ),

            'Макс. сердцебеение': cls.filter_by_date_and_equipment(
                db.func.max(
                    cls.max_heart_rate), id, start_date, end_date
            ),

            'Макс. температура': cls.filter_by_date_and_equipment(
                db.func.max(
                    cls.max_temperature), id, start_date, end_date
            ),

            'Макс. высота': cls.filter_by_date_and_equipment(
                db.func.max(
                    cls.max_altitude), id, start_date, end_date
            ),

            'Средний каденс': cls.filter_by_date_and_equipment(
                    db.func.sum(
                        cls.avg_cadence * cls.time) / db.func.sum(
                            cls.time), id, start_date, end_date
            ),

            'Среднее сердцебеение': cls.filter_by_date_and_equipment(
                    db.func.sum(
                        cls.avg_heart_rate * cls.time) / db.func.sum(
                            cls.time), id, start_date, end_date
            ),

            'Средняя скорость': cls.filter_by_date_and_equipment(
                (db.func.sum(
                    cls.distance) / Config.METERS_PER_KILOMETER) / (
                        db.func.sum(
                            cls.time) / Config.SECONDS_PER_MINUTE /
                        Config.MINUTES_PER_HOUR), id, start_date, end_date
            ),

            'Мин. температура': cls.filter_by_date_and_equipment(
                db.func.min(
                    cls.min_temperature), id, start_date, end_date
            ),

            'Мин. высота': cls.filter_by_date_and_equipment(
                db.func.min(
                    cls.min_altitude), id, start_date, end_date
            ),
        }
        return statistics

    @classmethod
    def histogram_data(cls, start_date, end_date, equipmeint_id):
        date = start_date
        date_list = [date]
        while date != end_date:
            date += timedelta(days=1)
            date_list.append(date)

        historam_data = {}

        for date in date_list:
            historam_data[date] = {
                'date': date.strftime('%Y.%m.%d'),
                'dist': 0
            }

        for data in Stats.stats_filter_by_date(
            equipmeint_id,
            start_date, end_date
        ):
            historam_data[data.date] = {
                'date': data.date.strftime('%Y.%m.%d'),
                'dist': data.distance / Config.METERS_PER_KILOMETER,
                'time': data.time
            }

        histogram_data = [x for x in historam_data.values()]
        return histogram_data


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
