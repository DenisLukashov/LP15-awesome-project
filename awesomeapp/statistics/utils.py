from datetime import timedelta
import os

from awesomeapp.equipment.models import EquipmentType
from config import Config


def convert_to_seconds(time):
    if not time:
        return None
    unit_of_time = [int(x) for x in time.split(':')]
    hours, minutes, seconds = unit_of_time
    time = timedelta(hours=hours, minutes=minutes, seconds=seconds)
    return int(time.total_seconds())


def convert_to_meter(value):
    return None if value is None else value * Config.METERS_PER_KILOMETER


def delete_images_from_disk(images):
    for image in images:
        file = image.src.split('/')[-1]
        file_path = os.path.join(
            Config.GLOBAL_PATH, Config.STORY_IMAGE_PATH, file)
        os.remove(file_path)


def convert_time_to_user_view(time):
    if time == 0:
        return time
    hours = time // Config.MINUTES_PER_HOUR // Config.SECONDS_PER_MINUTE
    minutes = time // Config.MINUTES_PER_HOUR % Config.SECONDS_PER_MINUTE
    seconds = time % Config.MINUTES_PER_HOUR % Config.SECONDS_PER_MINUTE
    return f'{hours}ч. {minutes}м. {seconds}с.'


def get_statistics_fields(equipment_type, form):
    step = {
        'Основные параметры': [
            form.date,
            form.distance,
            form.time,
        ],
        'Дополнительные параметры': [
            form.steps,
            form.max_speed,
            form.total_time,
        ],
        'Физическое состояние': [
            form.avg_cadence,
            form.max_cadence,
            form.avg_heart_rate,
            form.max_heart_rate,
        ],
        'Параметры окружающей среды': [
            form.max_temperature,
            form.min_temperature,
        ],
        'Рельеф местности': [
            form.start_altitude,
            form.total_up_altitude,
            form.total_down_altitude,
            form.min_altitude,
            form.max_altitude
        ],
    }
    bike = step.copy()

    bike_param = set(step.get('Дополнительные параметры')) - {form.steps}

    bike_param = [
        value
        for value in step.get('Дополнительные параметры')
        if value in bike_param
    ]
    bike['Дополнительные параметры'] = bike_param

    step_trainer = trainer(step)
    bike_trainer = trainer(bike)

    (
        walking,
        run,
        treadmill,
        skiing,
        skirollers,
        skates,
        bycicle,
        exercise_bike
    ) = [eq.id for eq in EquipmentType.query.all()]

    fields = {}
    fields[walking] = fields[run] = fields[skiing] = step
    fields[skirollers] = fields[skates] = step
    fields[treadmill] = step_trainer
    fields[bycicle] = bike
    fields[exercise_bike] = bike_trainer

    return fields.get(equipment_type)


def trainer(fields):
    new_fields = fields.copy()
    new_fields.pop('Рельеф местности')
    new_fields.pop('Параметры окружающей среды')
    return new_fields


def convert_none_to_int(data):
    return 0 if data is None else data
