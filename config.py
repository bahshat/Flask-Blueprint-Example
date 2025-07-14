import os

class Config:
    SECRET_KEY = 'your_secret_key'
    JWT_SECRET = 'your_jwt_signing_secret'
    DB_PATH = os.path.join(os.path.expanduser('~'), 'system_metrics.db')

class DevelopmentConfig(Config):
    DEBUG = True
    # Development-specific settings

class ProductionConfig(Config):
    DEBUG = False
    # Production-specific settings
