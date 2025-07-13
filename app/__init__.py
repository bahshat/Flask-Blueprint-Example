from flask import Flask
from app.extensions import jwt, socketio

# Import your blueprints
from app.routes.main import home_bp
from app.routes.auth import auth_bp
from app.routes.device import device_bp

# Import socket handlers
from app import sockets

def create_app(config_class='config.DevelopmentConfig'):
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(config_class)

    # Initialize extensions
    jwt.init_app(app)
    socketio.init_app(app)

    # Register blueprints
    app.register_blueprint(home_bp, url_prefix='/')
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
    app.register_blueprint(device_bp, url_prefix='/api/v1/device')

    return app