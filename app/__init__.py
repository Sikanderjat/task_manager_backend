from flask import Flask
from app.utils.db import db
from app.models import User, TaskManager, TaskLogger
from app.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    db.init_app(app)

    # Import routes AFTER initializing Flask
    from app.api.routes import api_bp
    app.register_blueprint(api_bp, url_prefix="/api")

    return app
