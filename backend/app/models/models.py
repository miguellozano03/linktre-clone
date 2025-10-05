from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Enum as SQLEnum
from ..config import db
from .roles import UserRole

class User(db.Model):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    nickname: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    role: Mapped[UserRole] = mapped_column(SQLEnum(UserRole), nullable=False, default=UserRole.USER)

    links: Mapped[list["Link"]] = relationship("Link", back_populates="user", cascade="all, delete-orphan")

    def __init__(self, username, password, nickname, email):
        self.username = username
        self.password = password
        self.nickname = nickname
        self.email = email

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            # "password": self.password,
            "nickname": self.nickname,
            "email": self.email,
            "links": [link.to_dict() for link in list(self.links)]  # pyright: ignore[reportAttributeAccessIssue]
        }
    
class Link(db.Model):
    __tablename__ = 'links'

    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(String(2080), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="links")

    def __init__(self, url, user, title=None):
        self.url = url
        self.title = title # type: ignore
        self.user = user

    def to_dict(self):
        return {
            "id": self.id,
            "url": self.url,
            "title": self.title
        }