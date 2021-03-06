from flask import Flask

from config import Config
from awesomeapp.user.models import User
from awesomeapp.extensions import db, login, migrate
from awesomeapp.statistics.views import blueprint as statistics_blueprint
from awesomeapp.equipment.views import blueprint as equipment_blueprint
from awesomeapp.user.views import blueprint as user_blueprint
from awesomeapp.vizit.views import blueprint as vizit_blueprint


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)

    login.init_app(app)
    login.login_view = 'user.login'

    migrate.init_app(app, db)

    app.register_blueprint(statistics_blueprint)
    app.register_blueprint(equipment_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(vizit_blueprint)

    @login.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    return app


app = create_app(Config)
