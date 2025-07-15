import json
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from datetime import datetime, timedelta
from app.services.database import get_historic_metrics

device_bp = Blueprint('device', __name__)

# Path to the devices JSON file
DEVICES_FILE = 'devices.json'

def load_device_info():
    """Load device information from the JSON file."""
    try:
        with open(DEVICES_FILE, 'r') as f:
            return json.load(f)['device']
    except (FileNotFoundError, json.JSONDecodeError):
        return None


@device_bp.route('/info', methods=['GET'])
@jwt_required()
def get_device_info():
    """Retrieve and return device information from the JSON file."""
    device_info = load_device_info()
    
    if not device_info:
        return jsonify({"msg": "Device information not found"}), 404

    return jsonify(device_info), 200


@device_bp.route('/history', methods=['GET'])
@jwt_required()
def get_device_parameter():
    start_time = request.args.get('start_time')
    if not start_time:
        return jsonify({"msg": "Start time is required"}), 400
    try:
        datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return jsonify({"msg": "Invalid start time format. Use 'YYYY-MM-DD HH:MM:SS'"}), 400
    
    print(f"current now: {datetime.now()}") 

    formatedTime = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
    end_time = formatedTime + timedelta(hours=1) # TODO: Post testing change this to 1 hour


    rows = get_historic_metrics(start_time, end_time)

    print(f"current now: {datetime.now()}") 
  
    if not rows:
        return jsonify({"msg": "No data found for the specified time range"}), 404
    
    # Convert rows to a list of dictionaries
    metrics = []
    for row in rows:
        metrics.append({
            "timestamp": row[0],
            "cpuUsage": row[1],
            "cpuTemp": row[2],
            "memUsed": row[3],
            "nwStatSent": row[4],
            "nwStatRecv": row[5]
        })
    
    return jsonify(metrics), 200