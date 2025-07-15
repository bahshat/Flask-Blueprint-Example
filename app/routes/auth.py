import json
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.utils.crypto import decrypt_data

auth_bp = Blueprint('auth', __name__)

# Path to the users JSON file
USERS_FILE = 'users.json'


def load_users():
    """Load users from the JSON file."""
    try:
        with open(USERS_FILE, 'r') as f:
            return json.load(f)['users']
    except (FileNotFoundError, json.JSONDecodeError):
        return []


@auth_bp.route('/login', methods=['POST'])
def login():
    """Authenticate a user and return a JWT token."""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"msg": "Username and password are required"}), 400

    users = load_users()
    user = next((u for u in users if u['username'] == username), None)

    if user and password == decrypt_data(user['password']):
        access_token = create_access_token(identity=username)
        return jsonify({"msg": "Login successful", "token": access_token}), 200
    
    return jsonify({"msg": "Bad username or password"}), 401


@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """Logout the user."""
    return jsonify({"message": "Logged out successfully"}), 200