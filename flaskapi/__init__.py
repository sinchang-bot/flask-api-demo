from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flaskapi.config import Config

db = SQLAlchemy()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from flaskapi.api import api_blueprint
    from flaskapi.errors.handlers import errors
    app.register_blueprint(api_blueprint)
    app.register_blueprint(errors)

    return app
