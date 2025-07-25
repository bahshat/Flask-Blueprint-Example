from app import create_app
from app.extensions import socketio
from config import DevelopmentConfig

app = create_app(DevelopmentConfig)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)