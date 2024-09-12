import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import config
from flask_login import LoginManager


# initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app(config_name):
    app = Flask(__name__)

    # APPLY CONFIGURATION FROM config.py
    app.config.from_object(config[config_name])
#    config[config_name].init_app(app)

    db.init_app(app)
    migrate.init_app(app,db)
    login_manager.init_app(app)
    login_manager.login_view = 'login' # Endpoint name for login

    # import models to ensure they are registered with SQLAlchemy
    with app.app_context():
        db.create_all()
    return app

@login_manager.user_loader
def load_user(user_id):
    from .models import User
    return User.query.get(int(user_id))