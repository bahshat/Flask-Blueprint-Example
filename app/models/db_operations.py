import sqlite3
import os

DB_PATH = None

def init_db(app):
    """Initialize the database."""
    global DB_PATH
    DB_PATH = app.config['DB_PATH']
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS metrics (
                    timestamp TEXT,
                    cpuUsage REAL,
                    cpuTemp REAL,
                    memUsed INTEGER,
                    nwStatSent INTEGER,
                    nwStatRecv INTEGER
                )''')
    conn.commit()
    conn.close()


def write_to_db(metrics):
    """Write the current metrics to the database."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO metrics VALUES (?, ?, ?, ?, ?, ?)", 
                       (metrics['timestamp'],
                        metrics['cpuUsage'],
                        metrics['cpuTemp'],
                        metrics['memUsed'],
                        metrics['nwStatSent'],
                        metrics['nwStatRecv']))
        conn.commit()
        conn.close()
    except Exception as e:
        # In a real application, you'd want to log this error.
        print(f"Failed to write to DB: {e}")


def get_historic_metrics(start_time, end_time):
    """Get historic metrics from the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM metrics WHERE timestamp BETWEEN ? AND ?", (start_time, end_time))
    rows = cursor.fetchall()
    conn.close()
    return rows