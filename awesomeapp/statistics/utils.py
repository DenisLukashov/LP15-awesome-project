from datetime import timedelta


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


def total_parametr_sum(parameter, matched):
    return sum( 0 if getattr(stat, parameter) is None  else getattr(stat, parameter) for stat in matched )


def convert_time_to_user_view(time):
    hours = time // 60 // 60
    minutes = time // 60 % 60
    seconds = time % 60 % 60
    return f'{hours}ч. {minutes}м. {seconds}с.'