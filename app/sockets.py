from flask_socketio import emit, join_room, leave_room
from app.extensions import socketio
from app.services import system_monitor

# Define room names
CURRENT_METRICS_ROOM = 'current_metrics_room'

def send_current_metrics(metrics):
    socketio.emit('current_metrics_response', metrics, room=CURRENT_METRICS_ROOM)

system_monitor.register_metrics_callback(send_current_metrics)


@socketio.on('connect')
def handle_connect():
    print('Client connected')


@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')


@socketio.on('join')
def on_join(data):    
    join_room(CURRENT_METRICS_ROOM)
    emit('status', {'msg': f'Joined {CURRENT_METRICS_ROOM}'}, room=CURRENT_METRICS_ROOM)


@socketio.on('leave')
def on_leave(data):    
    leave_room(CURRENT_METRICS_ROOM)
    emit('status', {'msg': f'Left {CURRENT_METRICS_ROOM}'}, room=CURRENT_METRICS_ROOM)