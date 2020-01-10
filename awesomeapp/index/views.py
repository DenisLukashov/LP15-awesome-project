from flask import Blueprint, render_template
from flask_login import current_user

from awesomeapp.equipment.models import Equipment
blueprint = Blueprint('index', __name__, template_folder='templates', url_prefix='/index')


@blueprint.route('/')
def index():
    equips = Equipment.query.filter(Equipment.user_id == current_user.id).all()
    for i in equips:
        print(i.name)
    return render_template('index/index.html', title='Главная страница', equips=equips)
