from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import config
# initialize extensions
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name):
    app = Flask(__name__)


    # APPLY CONFIGURATION FROM config.py
    app.config.from_object(config[config_name])
#    config[config_name].init_app(app)

    db.init_app(app)
    migrate.init_app(app,db)

    # import models to ensure they are registered with SQLAlchemy
    from .models import User, Addiction, Routine, Feedback
    return app
