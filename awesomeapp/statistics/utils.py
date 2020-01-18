from datetime import timedelta
from awesomeapp.statistics.forms import StatisticsForm
from awesomeapp.equipment.models import EquipmentType



def convert_to_seconds(time):
    if not time:
        return None
    unit_of_time = [int(x) for x in time.split(':')]
    if len(unit_of_time) < 3:
        unit_of_time.append(0)
    hours, minutes, seconds = unit_of_time
    time = timedelta(hours=hours, minutes=minutes, seconds=seconds)
    return int(time.total_seconds())


def convert_to_meter(value):
    return None if value is None else value * 1000


def total_parameter_sum(parameter, matched):
    return sum(0 if getattr(stat, parameter) is None else getattr(
                stat, parameter) for stat in matched)


def max_parameter(parameter, matched):
    return max([0 if getattr(stat, parameter) is None else getattr(
                stat, parameter) for stat in matched])


def avg_parameter(parameter, time_parameter, matched):
    parameters = [0 if getattr(stat, parameter) is None else getattr(
                stat, parameter) for stat in matched]
    time_parameters = [0 if getattr(stat, time_parameter) is None else getattr(
                stat, time_parameter) for stat in matched]
    return sum([param * time for param, time in zip(parameters,
                time_parameters)])//sum(time_parameters)


def convert_time_to_user_view(time):
    hours = time // 60 // 60
    minutes = time // 60 % 60
    seconds = time % 60 % 60
    return f'{hours}ч. {minutes}м. {seconds}с.'


def statistics_field(equipment_type):
    form = StatisticsForm()
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

    bike_param = [value for value in step.get('Дополнительные параметры') if value in bike_param]
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
    fields[walking] = fields[run] = fields[skiing] = fields[skirollers] = fields[skates] = step
    fields[treadmill] = step_trainer
    fields[bycicle] = bike
    fields[exercise_bike] = bike_trainer

    return fields.get(equipment_type)

def trainer(fields):
    new_fields = fields.copy()
    new_fields.pop('Рельеф местности')
    new_fields.pop('Параметры окружающей среды')
    return new_fields

