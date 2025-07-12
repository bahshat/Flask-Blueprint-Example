from flask import Flask
from app.extensions import jwt # Import the jwt object

# Import your blueprints
from app.routes.main import home_bp
from app.routes.auth import auth_bp
from app.routes.device import device_bp

def create_app(config_class='config.DevelopmentConfig'):
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(config_class)

     # Initialize extensions
    jwt.init_app(app) # Initialize Flask-JWT-Extended

    # Register blueprints
    app.register_blueprint(home_bp, url_prefix='/')  # Routes in main.py will start with frontend root
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth') # Routes in auth.py will start with /api/auth
    app.register_blueprint(device_bp, url_prefix='/api/v1/device') # Routes in device.py will start with /api/device

    # You could initialize extensions here if you had them, e.g., Flask-JWT-Extended
    # from flask_jwt_extended import JWTManager
    # jwt = JWTManager(app)

    return app