from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth_bp = Blueprint('auth', __name__)

# Hardcoded user for simplicity
HARDCODED_USERNAME = "admin"
HARDCODED_PASSWORD = "password123" # In real app, this would be hashed

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username != HARDCODED_USERNAME or password != HARDCODED_PASSWORD:
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username) # Create token
    return jsonify({"msg": "Login successful", "token": access_token}), 200


@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    # In a real app, handle token invalidation or client-side token removal
    return jsonify({"message": "Logged out successfully"}), 200