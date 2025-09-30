from ..config.database import db
from sqlalchemy.exc import SQLAlchemyError
from ..config.database import db
from ..models.models import Link, User


class LinkService():
    
    def __init__(self, username: str, link_data: dict | None = None) -> None:
        self.user = User.query.filter_by(username=username).first()
        self.link_data = link_data

    def get_all_user_links(self):
        
        if not self.user:
            return None
        try:
            links = Link.query.filter_by(user_id=self.user.id).all()
            link_list = [link.to_dict() for link in links]
            return link_list
        except SQLAlchemyError as e:
            raise e
    
    def create_link(self):
        if not self.user:
            return None
        if not self.link_data or "url" not in self.link_data:
            raise ValueError("URl is required to create a link.")
        try:
            new_link = Link(self.link_data["url"], self.user, title=self.link_data.get('title'))
            db.session.add(new_link)
            db.session.commit()
            return new_link
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
        
    def update_link(self, link_id: int):
        if not self.user:
            return None
        
        link = Link.query.filter_by(id=link_id, user_id=self.user.id).first()
        if not link:
            return None
        
        if not self.link_data:
            raise ValueError("No data provided to update the link.")

        try:
            if "url" in self.link_data:
                link.url = self.link_data["url"]
            if "title" in self.link_data:
                link.title = self.link_data["title"]
            
            db.session.commit()
            return link
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
        
    def delete_link(self, link_id: int):
        if not self.user:
            return False
        link = Link.query.filter_by(id=link_id, user_id=self.user.id).first()
        if not link:
            return False
        
        try:
            db.session.delete(link)
            db.session.commit()
            return link
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e