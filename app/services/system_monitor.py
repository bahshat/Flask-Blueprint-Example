import psutil
import threading
import time
from app.models.database import write_to_db
from datetime import datetime

DB_PATH = None
running = False
thread = None

metrics = {}
metrics_update_callback = None

def get_Metrics():
    return metrics

def capture_metrics():
    """Get the current system metrics."""
    temps = psutil.sensors_temperatures()
    cpu_temp = 0.0
    if temps:
        for name, entries in temps.items():
            for entry in entries:
                if 'cpu' in name.lower() or 'core' in entry.label.lower():
                    cpu_temp = entry.current
                    break
            if cpu_temp:
                break

    # TODO: Above nested logic must be simplified.

    mem = psutil.virtual_memory()
    net = psutil.net_io_counters()


    # Capture the current time in a specific format
    captured_at = datetime.now()
    captured_at = captured_at.strftime("%Y-%m-%d %H:%M:%S")
    
    return {
        'timestamp': captured_at,
        'cpuUsage': psutil.cpu_percent(interval=1),
        'cpuTemp': cpu_temp,
        'memUsed': mem.used,
        'nwStatSent': net.bytes_sent,
        'nwStatRecv': net.bytes_recv
    }

def register_metrics_callback(callback_func):
    global metrics_update_callback
    metrics_update_callback = callback_func

def start_logging(): 
    """Start logging the metrics in a background thread."""
    global running, thread
    if not running:
        running = True
        thread = threading.Thread(target=log_metrics)
        thread.daemon = True
        thread.start()

def log_metrics():
    """Continuously log metrics every second."""
    while running:
        global metrics
        metrics = capture_metrics()
        write_to_db(metrics)
        if metrics_update_callback: # New: Call the registered callback
            metrics_update_callback(metrics)
        time.sleep(1)