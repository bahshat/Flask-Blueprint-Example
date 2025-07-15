import sqlite3
from flask import current_app
import os

def get_historic_metrics(start_time, end_time):
    """Get historic metrics from the database."""
    conn = sqlite3.connect(current_app.config['DB_PATH'])
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM metrics WHERE timestamp BETWEEN ? AND ?", (start_time, end_time))
    rows = cursor.fetchall()
    conn.close()
    return rows