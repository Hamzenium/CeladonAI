from flask import Blueprint, request, jsonify
from services.db_service import save_to_firebase, get_user_documents, delete_document

user_blueprint = Blueprint('users', __name__)

@user_blueprint.route('/create/user', methods=['POST'])
def create_user():
    try:
        email = request.json["email"]
        data = {"name": request.json["name"], "email": email, "files": []}
        save_to_firebase(data, email)
        return jsonify({"message": "User created successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
