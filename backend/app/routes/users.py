from flask import Blueprint, jsonify, request
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash
from ..models.models import User
from ..config.database import db

users_bp = Blueprint('users_bp', __name__)

@users_bp.route('/users', methods=['GET'])
def get_users():
    """
    Retrieves all users from the database.
    """
    users = User.query.all()
    users_list = [user.to_dict() for user in users]
    return jsonify(users_list)

@users_bp.route('/users/<string:username>', methods=['GET'])
def get_user(username: str):
    """
    Retrieves an user by username
    """
    try: 
        stmt = select(User).where(User.username == username)
        result = db.session.execute(stmt)
        user = result.scalar_one_or_none()

        if user:
            return jsonify({"user": user.to_dict()})
        else:
            return jsonify({"message": "User not found."}),404
        
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 400

@users_bp.route('/users', methods=['POST'])
def create_user(): 
    data = request.get_json()

    try:
        #Crear funcion o un helper en el futuro para mejorar la escalabilidad en ves de usar eso directo.
        hashed_password = generate_password_hash(data['password'])
        #Faltan validaciones importantes
        new_user = User(username=data['username'], password=hashed_password, nickname=data['nickname'], email=data['email'])
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": f"New user with id: {new_user.id}"}), 201
    
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 400
    
@users_bp.route('/users/<string:username>', methods=['PUT'])    
def replace_user(username: str):
    data = request.get_json()
    user = User.query.filter_by(username=username).first()
    
    if not user:
        return jsonify({"message": "User not found."}), 404
    
    try:
        user.username = data['username']
        user.password = data['password']
        user.nickname = data['nickname']
        user.email = data['email']

        if 'password' in data:
            user.password = generate_password_hash(data['password'])

        
        db.session.commit()
        return jsonify({"message": "User replaced", "user": user.to_dict()})
    
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 400

@users_bp.route('/users/<string:username>', methods=['PATCH'])
def edit_user(username: str):
    data = request.get_json()
    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({"message": "User not found"}), 404
    
    try:
        if "username" in data:
            user.username = data["username"]
        if "password" in data:
            user.password = generate_password_hash(data['password'])
        if "nickname" in data:
            user.nickname = data["nickname"]
        if "email" in data:
            user.email = data["email"]
        db.session.commit()
        return jsonify({"message": "User updated.", "user": user.to_dict()})
    
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 400
    
@users_bp.route('/users/<string:username>', methods=['DELETE'])
def delete_user(username: str):
    try:
        stmt = select(User).where(User.username == username)
        result = db.session.execute(stmt)
        user = result.scalar_one_or_none()
        
        if user:
            db.session.delete(user)
            db.session.commit()
            return jsonify({"message": f"The user with id: {user.id} was deleted"})
        else:
            return({"message": "User not found."})

    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 400