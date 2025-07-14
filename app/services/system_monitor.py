import psutil
import threading
import time
from app.services.database import write_to_db


DB_PATH = None
running = False
thread = None

metrics = {}

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
    
    # TODO: Above nested logic must be simplified.

    mem = psutil.virtual_memory()
    net = psutil.net_io_counters()

    return {
        'cpuUsage': psutil.cpu_percent(interval=1),
        'cpuTemp': cpu_temp,
        'memUsed': mem.used,
        'nwStatSent': net.bytes_sent,
        'nwStatRecv': net.bytes_recv
    }

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
        time.sleep(1)

