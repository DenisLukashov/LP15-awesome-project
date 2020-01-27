from datetime import timedelta

from sqlalchemy.orm import backref
from sqlalchemy import case

from awesomeapp.extensions import db
from config import Config
from awesomeapp.statistics.utils import (
    convert_time_to_user_view,
    convert_none_to_int
)


class Stats(db.Model):
    __tablename__ = 'stats'
    id = db.Column(db.Integer, primary_key=True)

    equipment_id = db.Column(
      db.Integer,
      db.ForeignKey('equipment.id'),
      index=True
    )
    equipment = db.relationship(
        'Equipment',
        backref=backref('stats', cascade='all,delete')
    )

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
      db.ForeignKey('stories.id'),
      index=True
    )

    story = db.relationship(
        'Story',
        uselist=False,
        cascade='all,delete',
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
    def filter_by_date(cls, id, start_date, end_date):
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
    def get_story_and_images(cls, id, start_date, end_date):
        if start_date != end_date:
            return None

        query = cls.query.filter(
                cls.equipment_id == id
            ).filter(
                cls.date == start_date
            ).first().story

        if query is None:
            return {'story': None, 'main_image': None}

        story_and_images = {'story': None if query.text == '' else query.text}

        if query.images == []:
            story_and_images['main_image'] = None
        else:
            main_image, *rest_images = [
                image.src for image in query.images
            ]
            story_and_images['main_image'] = main_image
            story_and_images['rest_images'] = rest_images

        return story_and_images

    @classmethod
    def get_statistics(cls, id, start_date, end_date, ):
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
                            case(
                                [
                                    (cls.avg_cadence.isnot(None), Stats.time),
                                    (cls.avg_cadence.is_(None), 0)
                                ]
                            )
                        ),
                    id, start_date, end_date
                ),

            'Среднее сердцебеение': cls.filter_by_date_and_equipment(
                    db.func.sum(
                        cls.avg_heart_rate * cls.time) / db.func.sum(
                            cls.time), id, start_date, end_date
            ),

            'Средняя скорость': cls.filter_by_date_and_equipment(
                db.func.round((db.func.sum(
                    cls.distance) / Config.METERS_PER_KILOMETER) / (
                        db.func.sum(
                            cls.time) / Config.SECONDS_PER_MINUTE /
                        Config.MINUTES_PER_HOUR), 2), id, start_date, end_date
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

        delta = end_date - start_date
        date_range = [start_date + timedelta(x) for x in range(delta.days + 1)]

        histogram_data = {
            date: {
                'Дата': date.strftime('%Y.%m.%d'),
                'Дистанция': 0
            }
            for date in date_range
        }

        for data in Stats.filter_by_date(
            equipmeint_id,
            start_date,
            end_date
        ):
            date = data.date.strftime('%Y.%m.%d')
            distance = (
                convert_none_to_int(data.distance) /
                Config.METERS_PER_KILOMETER
            )
            time = convert_none_to_int(data.time)
            try:
                speed = round(
                    distance / time *
                    Config.SECONDS_PER_MINUTE *
                    Config.MINUTES_PER_HOUR, 2
                )
            except ZeroDivisionError:
                speed = 0

            histogram_data[data.date] = {
                'Дата': date,
                'Дистанция': distance,
                'Время': convert_time_to_user_view(time),
                'Скорость': speed
            }

        histogram_data = list(histogram_data.values())
        return histogram_data


class Story(db.Model):
    __tablename__ = 'stories'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)

    stats_id = db.Column(
        db.Integer,
        db.ForeignKey('stats.id'),
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
    story = db.relationship('Story', backref=backref(
        'images', cascade='all,delete'))
