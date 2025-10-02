from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from .service import LinkService

links_bp = Blueprint('links_bp', __name__)

@links_bp.route('/links', methods=['GET'])
@jwt_required()
def get_links_endpoint():
    current_user = get_jwt_identity()

    service = LinkService(username=current_user)
    links = service.get_all_user_links()
    if links is None:
        return jsonify({"message": "User not found"}), 400
    
    return jsonify(links)
        

@links_bp.route('/links', methods=['POST'])
@jwt_required()
def create_link_endpoint():

    current_user = get_jwt_identity()
    data = request.get_json()

    service = LinkService(username=current_user, link_data=data)

    try:
        new_link = service.create_link()
        if new_link is None:
            return jsonify({"message": "User not found"}), 400
        return jsonify(new_link.to_dict()), 201
    
    except ValueError as e:
        return jsonify({"error": str(e)}),400
    

@links_bp.route('/links/<int:link_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def edit_link_endpoint(link_id: int):
    current_user = get_jwt_identity()
    data = request.get_json()
    service = LinkService(username=current_user, link_data=data)
    
    updated = service.update_link(link_id)
    if updated:
        return jsonify(updated.to_dict()), 200
    return jsonify({"message": "Link not found"}),400


@links_bp.route('/links/<int:link_id>', methods=['DELETE'])
@jwt_required()
def delete_link_endpoint(link_id: int):
    current_user = get_jwt_identity()
    data = request.get_json()
    service = LinkService(username=current_user, link_data=data)

    try:
        deleted = service.delete_link(link_id)
        if deleted:
            return jsonify(deleted.to_dict()), 200
        return jsonify({"message": "Link not found."}), 400
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 400