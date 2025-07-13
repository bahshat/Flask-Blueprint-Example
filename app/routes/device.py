import json
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

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