from flask import Blueprint, jsonify, request
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from ..config.database import db
from ..models.models import Link, User

links_bp = Blueprint('links_bp', __name__)

@links_bp.route('/links/<string:username>', methods=['GET'])
def get_links(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({"message": "User not found"}), 404

    links = Link.query.filter_by(user_id=user.id).all() # type: ignore

    link_list = [link.to_dict() for link in links]

    return jsonify(link_list)

@links_bp.route('/users/<string:username>/links', methods=['POST'])
def create_link(username):
    data = request.get_json()
    if not 'url' in data:
        return jsonify({"error": "URL is required"}), 400
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "User not found"}), 400
    
    try:
        new_link = Link(url=data['url'], user=user, title=data.get('title'))
        db.session.add(new_link)
        db.session.commit()

        return jsonify({"message": f"Link created {new_link.to_dict()} "}), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
