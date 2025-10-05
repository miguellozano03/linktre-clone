from .service import get_all_users, get_user, create_user, update_user, delete_user
from ..models import UserRole

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from sqlalchemy.exc import SQLAlchemyError

users_bp = Blueprint('users_bp', __name__)

@users_bp.route('/users', methods=['GET'])
@jwt_required()
def get_users_endpoint():
    """
    Endpoint to retrieve all users stored in the database

    Calls the service layer function `get_all_users`` to fetch the data.

    Returns:
        JSON: A list of user dictionaries
    """
    claims = get_jwt()
    
    if claims.get('role') != UserRole.ADMIN.value:
        return jsonify({"message": "Authorized personnel only"}), 403

    return jsonify(get_all_users())


@users_bp.route('/users/@<string:username>', methods=['GET'])
def get_user_endpoint(username: str):
    """
    Show a User by username
    """
    user = get_user(username)
    if user:
        return jsonify(user)
    return jsonify({"message": "User not found"}), 404


@users_bp.route('/users', methods=['POST'])
def create_user_endpoint():
    try:
        json_data = request.get_json()
        if not isinstance(json_data, dict):
            return jsonify({"error": "Invalid JSON"}), 400

        # Validación manual mínima
        required_fields = ["username", "password", "nickname", "email"]
        for f in required_fields:
            if f not in json_data:
                return jsonify({"error": f"Missing field: {f}"}), 400

        # Crear usuario llamando al servicio
        new_user = create_user(json_data)

        # Serializar a dict sin Marshmallow
        return jsonify({
            "id": new_user.id,
            "username": new_user.username,
            "nickname": new_user.nickname,
            "email": new_user.email,
            "role": new_user.role.value
        }), 201

    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 400


@users_bp.route('/users/me', methods=['PUT', 'PATCH'])
@jwt_required()
def edit_user_endpoint():
    current_user = get_jwt_identity()

    data = request.get_json()
    updated = update_user(data, current_user)

    if updated:
        return jsonify(updated.to_dict())
    
    return jsonify({"message": "User not found"}),404
    

@users_bp.route('/users/<string:username>', methods=['DELETE'])
@jwt_required()
def delete_user_endpoint(username):
    claims = get_jwt()
    current_user = get_jwt_identity()

    if current_user != username and claims.get('role') != UserRole.ADMIN.value:
        return jsonify({"message": "Unauthorized"}), 403

    deleted = delete_user(username)
    if deleted:
        return jsonify(deleted.to_dict())

    return jsonify({"message": "User not found"}),404