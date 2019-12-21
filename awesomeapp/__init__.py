from config import Config
from flask import Flask, send_from_directory, current_app
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__, static_url_path='/static')
app.config.from_object(Config)

login = LoginManager(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from awesomeapp import views, models
