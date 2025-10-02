from typing import cast

from ..config.database import db
from ..models.models import User
from ..utils.security import hash_password

from sqlalchemy.exc import SQLAlchemyError


def save_user(user):
    """
    Saves an user in the database.
    """
    db.session.add(user)
    db.session.commit()
    return user


def get_all_users():
    """
    Retrieves all users stored in the database

    Returns:
        list: A list of users, each represented as a dictionary using the `to_dict` method.
    """
    try:
        users = User.query.all()
        users_list = [user.to_dict() for user in users]
        return users_list
    except SQLAlchemyError as e:
        raise e


def get_user(username):
    try:
        user = User.query.filter_by(username=username).first()

        if user:
            return user.to_dict()
        else:
            return None
        
    except SQLAlchemyError as e:
        raise e


def create_user(user_data: dict):
    try: 
        user_data['password'] = hash_password(user_data['password'])
        new_user = User(**user_data)
        db.session.add(new_user)
        db.session.commit()
        return new_user
    
    except SQLAlchemyError as e:
        db.session.rollback()
        raise e


def update_user(user_data: dict, username: str):
    user = User.query.filter_by(username=username).first()
    if not user:
        return None
    
    try:
        if "username" in user_data:
            user.username = user_data['username']
        if 'password' in user_data:
            user.password = hash_password(user_data['password'])
        if "nickname" in user_data:
            user.nickname = user_data['nickname']
        if "email" in user_data:
            user.email = user_data['email']
        
        db.session.commit()
        return user
        
    except SQLAlchemyError as e:
        db.session.rollback()
        raise e
    
    
def delete_user(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return None
    try:
        db.session.delete(user)
        db.session.commit()
        return user
    except SQLAlchemyError as e:
        raise e