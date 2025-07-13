import psutil

def get_current_metrics():
    """Get the current system metrics."""
    temps = psutil.sensors_temperatures()
    cpu_temp = 0.0
    if temps:
        for name, entries in temps.items():
            for entry in entries:
                if 'cpu' in name.lower() or 'core' in entry.label.lower():
                    cpu_temp = entry.current
                    break

    mem = psutil.virtual_memory()
    net = psutil.net_io_counters()

    return {
        'cpuUsage': psutil.cpu_percent(interval=1),
        'cpuTemp': cpu_temp,
        'memUsed': mem.used,
        'nwStatSent': net.bytes_sent,
        'nwStatRecv': net.bytes_recv
    }