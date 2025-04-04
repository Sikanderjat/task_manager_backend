import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify
from werkzeug.security import check_password_hash
from app.models.user import User
from app.utils.db import db
from app.config import Config

class Security:
    @staticmethod
    def generate_token(user_id, roles=None):
        """Generate JWT token for authenticated user"""
        payload = {
            'exp': datetime.utcnow() + timedelta(hours=Config.JWT_EXPIRATION_HOURS),
            'iat': datetime.utcnow(),
            'sub': user_id,
            'roles': roles or []
        }
        return jwt.encode(
            payload,
            Config.JWT_SECRET_KEY,
            algorithm='HS256'
        )

    @staticmethod
    def decode_token(token):
        """Decode and verify JWT token"""
        try:
            payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=['HS256'])
            return payload['sub'], payload['roles']
        except jwt.ExpiredSignatureError:
            return None, ['token_expired']
        except jwt.InvalidTokenError:
            return None, ['invalid_token']

    @staticmethod
    def auth_required(f):
        """Decorator for routes requiring authentication"""
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None
            
            if 'Authorization' in request.headers:
                token = request.headers['Authorization'].split(" ")[1]

            if not token:
                return jsonify({'message': 'Token is missing'}), 401

            user_id, roles = Security.decode_token(token)
            if not user_id:
                return jsonify({'message': 'Token is invalid or expired'}), 401

            current_user = User.query.get(user_id)
            if not current_user or not current_user.is_active:
                return jsonify({'message': 'User not found or inactive'}), 401

            return f(current_user, *args, **kwargs)
        return decorated

    @staticmethod
    def roles_required(*required_roles):
        """Decorator for routes requiring specific roles"""
        def decorator(f):
            @wraps(f)
            def decorated(current_user, *args, **kwargs):
                if not any(role in current_user.roles for role in required_roles):
                    return jsonify({'message': 'Insufficient permissions'}), 403
                return f(current_user, *args, **kwargs)
            return decorated
        return decorator

    @staticmethod
    def permissions_required(*required_permissions):
        """Decorator for routes requiring specific permissions"""
        def decorator(f):
            @wraps(f)
            def decorated(current_user, *args, **kwargs):
                if not current_user.can(required_permissions):
                    return jsonify({'message': 'Insufficient permissions'}), 403
                return f(current_user, *args, **kwargs)
            return decorated
        return decorator
