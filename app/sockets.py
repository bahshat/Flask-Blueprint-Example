from flask_socketio import emit, join_room, leave_room
from app.extensions import socketio
from app.services.system_monitor import get_current_metrics
from app.services.historic_data import get_historic_metrics

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('join')
def on_join(data):
    room = data['room']
    join_room(room)
    emit('status', {'msg': 'Joined room ' + room}, room=room)

@socketio.on('leave')
def on_leave(data):
    room = data['room']
    leave_room(room)
    emit('status', {'msg': 'Left room ' + room}, room=room)

@socketio.on('get_current_metrics')
def handle_get_current_metrics(data):
    room = data.get('room')
    if room:
        metrics = get_current_metrics()
        emit('current_metrics_response', metrics, room=room)

@socketio.on('get_historic_metrics')
def handle_get_historic_metrics(data):
    room = data.get('room')
    start_time = data.get('start_time')
    end_time = data.get('end_time')

    if room and start_time and end_time:
        def background_task():
            for chunk in get_historic_metrics(start_time, end_time):
                emit('historic_data_chunk', chunk, room=room)
                socketio.sleep(0.1) # Yield to other tasks
            emit('historic_data_finished', room=room)

        socketio.start_background_task(background_task)