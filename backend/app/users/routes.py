from .service import get_all_users, get_user, create_user, update_user, delete_user
from flask import Blueprint, jsonify, request
from sqlalchemy.exc import SQLAlchemyError


users_bp = Blueprint('users_bp', __name__)

@users_bp.route('/users', methods=['GET'])
def get_users_endpoint():
    """
    Endpoint to retrieve all users stored in the database

    Calls the service layer function `get_all_users`` to fetch the data.

    Returns:
        JSON: A list of user dictionaries
    """
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

    data = request.get_json()

    try:
        user = create_user(data)
        return jsonify(user.to_dict()), 201
    
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 400


@users_bp.route('/users/<string:username>', methods=['PUT', 'PATCH'])    
def edit_user_endpoint(username: str):

    data = request.get_json()
    updated = update_user(data,username)

    if updated:
        return jsonify(updated.to_dict())
    
    return jsonify({"message": "User not found"}),404
    

@users_bp.route('/users/<string:username>', methods=['DELETE'])
def delete_user_endpoint(username: str):
    deleted = delete_user(username)
    if deleted:
        return jsonify(deleted.to_dict())

    return jsonify({"message": "User not found"}),404