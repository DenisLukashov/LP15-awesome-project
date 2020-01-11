from flask import Blueprint, render_template
from flask_login import current_user

from awesomeapp.equipment.models import Equipment
from awesomeapp.utils import get_equips
blueprint = Blueprint('index', __name__, template_folder='templates', url_prefix='/index')


@blueprint.route('/')
def index():
    return render_template('index/index.html', title='Главная страница', equips=get_equips())
