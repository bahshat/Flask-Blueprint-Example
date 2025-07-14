from flask import Flask
from app.extensions import jwt, socketio
from app.services import system_monitor
from app import sockets

# blueprints
from app.routes.main import home_bp
from app.routes.auth import auth_bp
from app.routes.device import device_bp
from app.services.database import init_db


def create_app(config_class='config.DevelopmentConfig'):
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(config_class)

    # Initialize extensions
    jwt.init_app(app)
    socketio.init_app(app)

    # Initialize the database and start logging
    with app.app_context():
        init_db(app)
        system_monitor.start_logging()

    # Register blueprints
    app.register_blueprint(home_bp, url_prefix='/')
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
    app.register_blueprint(device_bp, url_prefix='/api/v1/device')

    return app