from flask import Blueprint, request, jsonify

home_bp = Blueprint('home', __name__)


@home_bp.route('/', methods=['GET'])
def login():
    # TODO: Implement Frontend servering logic
    # This route is intended to serve the frontend application
    # For now, it will return a simple message
    return jsonify({"message": "Frontend will be servered here"}), 200