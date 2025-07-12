from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity # Import for protection

device_bp = Blueprint('device', __name__)

# Dummy data for demonstration
DUMMY_DEVICE_INFO = {"serial": "QC12345", "model": "SolarPanelX", "firmware": "1.0.1"}


@device_bp.route('/info', methods=['GET'])
@jwt_required() # <--- This decorator protects the route
def get_device_info():
    # In a real app, add JWT authentication middleware here
    return jsonify(DUMMY_DEVICE_INFO), 200