from flask import Blueprint, jsonify, request
from app.models.user import User
from app.utils.db import db

api_bp = Blueprint("api", __name__)

@api_bp.route("/health", methods=["GET"])
def health_check():
    return {"status": "ok"}

@api_bp.route("/", methods=["GET"])
def home():
    return {"message": "Welcome to the API!"}

@api_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    
    # Required fields
    required_fields = ['username', 'email', 'password', 'first_name', 'last_name']
    if not all(field in data for field in required_fields):
        return jsonify({"message": "Missing required fields"}), 400

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    first_name = data.get("first_name")
    last_name = data.get("last_name")

    # Check if user already exists
    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
        return jsonify({"message": "User already exists."}), 400

    # Create new user with all fields
    new_user = User(
        username=username,
        email=email,
        first_name=first_name,
        last_name=last_name,
        phone_number=data.get("phone_number"),
        profile_image_url=data.get("profile_image_url")
    )
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "message": "User created successfully",
        "user": {
            "username": username,
            "email": email,
            "first_name": first_name,
            "last_name": last_name
        }
    }), 201
