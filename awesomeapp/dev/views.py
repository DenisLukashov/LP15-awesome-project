from flask import (
    Blueprint,
    redirect, 
    render_template, 
    send_from_directory, 
    url_for
)
from flask_login import current_user

from awesomeapp.utils import get_last_qeuip
from config import Config

blueprint = Blueprint('dev', __name__, template_folder='templates')


@blueprint.route('/static/<path>/<filename>')
def send_static(path, filename):
    return send_from_directory(f'{Config.STATIC_FOLDER}/{path}', filename)


@blueprint.route('/')
def start_page():
    if current_user.is_authenticated:
        last_qeuip = get_last_qeuip()
        if last_qeuip:
           return redirect(url_for('statistics.add', id=last_qeuip.id))
        return redirect(url_for('equipment.equipment'))
    else:
        return redirect(url_for('user.visit'))
