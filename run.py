from app import create_app
from config import DevelopmentConfig

app = create_app(DevelopmentConfig)

if __name__ == '__main__':
    # Flask-SocketIO integration would go here, wrapping the app
    # For now, simple Flask run
    app.run(host='0.0.0.0', port=5000)