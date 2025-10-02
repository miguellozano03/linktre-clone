from .service import get_all_users, get_user, create_user, update_user, delete_user
from ..models import UserRole
from ..schemas.schemas import UserSchema
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError

user_schema = UserSchema()

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


@users_bp.route('/users/<string:username>', methods=['GET'])
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
        # Obtener JSON y validar que sea un diccionario
        json_data = request.get_json()
        if not isinstance(json_data, dict):
            return jsonify({"error": "Invalid JSON"}), 400

        # Validar y deserializar con Marshmallow
        payload: dict = user_schema.load(json_data)
        
        # Llamar al servicio que crea el usuario
        new_user = create_user(payload)

        # Serializar la respuesta
        return user_schema.dump(new_user), 201

    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
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