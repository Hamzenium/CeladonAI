from functools import wraps
from flask import request, jsonify

def authenticate(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Unauthorized'}), 401
        # Add your authentication logic
        return f(*args, **kwargs)
    return decorated_function
