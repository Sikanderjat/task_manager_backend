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
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    # Check if user already exists
    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
        return jsonify({"message": "User already exists."}), 400

    # Create new user
    new_user = User(username=username, email=email)
    new_user.set_password(password)  # Assuming set_password method exists
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created successfully."}), 201
