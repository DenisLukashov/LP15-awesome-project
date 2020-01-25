from flask import (
    Blueprint,
    redirect,
    send_from_directory,
    url_for
)
from flask_login import current_user

from config import Config
from awesomeapp.equipment.models import Equipment

blueprint = Blueprint('dev', __name__, template_folder='templates')


@blueprint.route('/static/<path>/<filename>')
def send_static(path, filename):
    return send_from_directory(f'{Config.STATIC_FOLDER}/{path}', filename)


@blueprint.route('/')
def start_page():
    if current_user.is_authenticated:
        last_equipment = Equipment.get_first(current_user.id)
        if last_equipment:
            return redirect(url_for('statistics.menu', id=last_equipment.id))
        return redirect(url_for('equipment.equipment'))
    else:
        return redirect(url_for('user.visit'))
