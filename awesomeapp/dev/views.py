from flask import Blueprint, render_template, send_from_directory
from flask_login import login_required

from config import Config

blueprint = Blueprint('dev', __name__,template_folder='templates')


@blueprint.route('/')
def index():
    return render_template('dev/index.html')


@blueprint.route('/static/<path>/<filename>')
def send_static(path, filename):
    return send_from_directory(f'{Config.STATIC_FOLDER}/{path}', filename)
