import json
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from datetime import datetime, timedelta
from app.models.db_operations import get_historic_metrics
from app.models.data_manuplation import add_column_names

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
    
    formatedTime = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
    end_time = formatedTime + timedelta(hours=1) 
    rows = get_historic_metrics(start_time, end_time)

    if not rows:
        return jsonify({"msg": "No data found for the specified time range"}), 404
    
    metrics = add_column_names(rows)
    
    return jsonify(metrics), 200


