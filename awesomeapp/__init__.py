from flask import Flask

from config import Config
from awesomeapp.user.models import User
from awesomeapp.extensions import db, login, migrate
from awesomeapp.statistics.views import blueprint as statistics_blueprint
from awesomeapp.equipment.views import blueprint as equipment_blueprint
from awesomeapp.user.views import blueprint as user_blueprint
from awesomeapp.dev.views import blueprint as dev_blueprint


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    login.init_app(app)
    login.login_view = 'user.login'

    migrate.init_app(app, db)

    app.register_blueprint(statistics_blueprint)
    app.register_blueprint(equipment_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(dev_blueprint)

    @login.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    return app


app = create_app()
