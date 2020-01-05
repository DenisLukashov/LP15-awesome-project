from flask import Blueprint, render_template

blueprint = Blueprint('index', __name__, template_folder='templates', url_prefix='/index')


@blueprint.route('/')
def index():
    return render_template('index/index.html', title='Главная страница')
