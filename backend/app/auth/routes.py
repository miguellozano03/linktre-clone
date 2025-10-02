from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity

from ..models import User
from ..utils import verify_password

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/login', methods=['POST'])
def login_endpoint():
    data = request.get_json()

    user = User.query.filter_by(username=data.get('username')).first()
    
    if not user or not verify_password(data.get('password'), user.password):
        return jsonify({"message": "Username or password incorrect"}), 401
    access_token = create_access_token(identity=user.username)
    refresh_token = create_refresh_token(identity=user.username)
    return jsonify(access_token=access_token, refresh_token=refresh_token)

@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token)

