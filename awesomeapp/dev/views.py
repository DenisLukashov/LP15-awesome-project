from flask import (
    send_from_directory, 
    Blueprint,
    render_template, 
    redirect, 
    url_for
)
from flask_login import current_user
from config import Config
from awesomeapp.utils import get_last_qeuip

blueprint = Blueprint('dev', __name__, template_folder='templates')


@blueprint.route('/static/<path>/<filename>')
def send_static(path, filename):
    return send_from_directory(f'{Config.STATIC_FOLDER}/{path}', filename)
    # return send_from_directory(f'static/{path}', filename)

@blueprint.route('/')
def start_page():
    if current_user.is_authenticated:
        last_qeuip = get_last_qeuip()
        if last_qeuip:
           return redirect(url_for('statistics.add', id=last_qeuip.id))
        return redirect(url_for('equipment.equipment'))
    else:
        return redirect(url_for('user.visit'))
