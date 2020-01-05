from flask import send_from_directory, Blueprint

from config import Config

blueprint = Blueprint('dev', __name__, template_folder='templates')


@blueprint.route('/static/<path>/<filename>')
def send_static(path, filename):
    return send_from_directory(f'{Config.STATIC_FOLDER}/{path}', filename)
