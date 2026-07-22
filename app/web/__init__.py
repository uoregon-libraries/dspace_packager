import logging
import os
from dotenv import load_dotenv
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask.logging import default_handler
from config import DevelopmentConfig

load_dotenv()

def create_app():
    # Create the Flask application
    app = Flask(__name__)

    config_type = os.getenv('CONFIG_TYPE', default = DevelopmentConfig)
    app.config.from_object(config_type)
    app.logger.addHandler(logging.FileHandler(os.path.join(app.instance_path, "log")))
    app.logger.setLevel(logging.INFO)
    app.logger.info("Starting the packager web service")

    register_blueprints(app)
    return app

def register_blueprints(app):
    # register Flask Blueprints to the created app instance
    from web.views import view_blueprint

    app.register_blueprint(view_blueprint)
