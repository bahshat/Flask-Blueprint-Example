from flask_socketio import emit, join_room, leave_room
from app.extensions import socketio
from app.services.historic_data import get_historic_metrics
from app.services.system_monitor import get_Metrics


# Define room names
CURRENT_METRICS_ROOM = 'current_metrics_room'
HISTORIC_DATA_ROOM = 'historic_data_room'

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('join')
def on_join(data):
    device_type = data.get('device_type', 'web')  # Default to 'web'
    
    join_room(CURRENT_METRICS_ROOM)
    emit('status', {'msg': f'Joined {CURRENT_METRICS_ROOM}'})

    if device_type == 'mobile':
        join_room(HISTORIC_DATA_ROOM)
        emit('status', {'msg': f'Joined {HISTORIC_DATA_ROOM}'})


@socketio.on('leave')
def on_leave(data):
    device_type = data.get('device_type', 'web')
    
    leave_room(CURRENT_METRICS_ROOM)
    emit('status', {'msg': f'Left {CURRENT_METRICS_ROOM}'})
    
    if device_type == 'mobile':
        leave_room(HISTORIC_DATA_ROOM)
        emit('status', {'msg': f'Left {HISTORIC_DATA_ROOM}'})


@socketio.on('get_current_metrics')
def handle_get_current_metrics():
    metrics = get_Metrics()
    emit('current_metrics_response', metrics, room=CURRENT_METRICS_ROOM)

@socketio.on('get_historic_metrics')
def handle_get_historic_metrics(data):
    start_time = data.get('start_time')
    end_time = data.get('end_time')

    if start_time and end_time:
        def background_task():
            for chunk in get_historic_metrics(start_time, end_time):
                emit('historic_data_chunk', chunk, room=HISTORIC_DATA_ROOM)
                socketio.sleep(0.1)  # Yield to other tasks
            emit('historic_data_finished', room=HISTORIC_DATA_ROOM)

        socketio.start_background_task(background_task)