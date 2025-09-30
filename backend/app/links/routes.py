from flask import Blueprint, jsonify, request
from .service import LinkService

links_bp = Blueprint('links_bp', __name__)

@links_bp.route('/links/<string:username>', methods=['GET'])
def get_links(username):
    service = LinkService(username=username)
    links = service.get_all_user_links()
    if links is None:
        return jsonify({"message": "User not found"}), 400
    return jsonify(links)
        

@links_bp.route('/links/<string:username>', methods=['POST'])
def create_link(username):
    data = request.get_json()
    service = LinkService(username=username, link_data=data)
    try:
        new_link = service.create_link()
        if new_link is None:
            return jsonify({"message": "User not found"}), 400
        return jsonify(new_link.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}),400
    

@links_bp.route('/links/<string:username>/<int:link_id>', methods=['PUT', 'PATCH'])
def edit_link(username, link_id):
    data = request.get_json()
    service = LinkService(username=username, link_data=data)
    
    updated = service.update_link(link_id)
    if updated:
        return jsonify(updated.to_dict()), 200
    return jsonify({"message": "Link not found"}),400

@links_bp.route('/links/<string:username>/<int:link_id>', methods=['DELETE'])
def delete_link(username, link_id):
    data = request.get_json()
    service = LinkService(username=username, link_data=data)
    try:
        deleted = service.delete_link(link_id)
        if deleted:
            return jsonify(deleted.to_dict()), 200
        return jsonify({"message": "Link not found."}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400