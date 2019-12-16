from flask import Flask, render_template
from flask_migrate import Migrate

from .models import db

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('../config.py')
    db.init_app(app)
    migrate = Migrate(app, db)
    return app