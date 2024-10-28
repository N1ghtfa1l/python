from sqlalchemy import Integer, String, ForeignKey, TEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base

Base: DeclarativeMeta = declarative_base()


class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(
        String(length=1000), nullable=False)
    name: Mapped[str] = mapped_column(String(length=100), nullable=False)
    is_active: Mapped[bool] = mapped_column(nullable=False, default=False)
    role: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String(length=500), nullable=True)

    posts: Mapped[list["Post"]] = relationship(
        "Post", back_populates="user", cascade="all, delete-orphan")


class Post(Base):
    __tablename__ = 'post'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(TEXT, nullable=False)
    description: Mapped[str] = mapped_column(TEXT)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('user.id', ondelete="CASCADE"))

    user: Mapped["User"] = relationship("User", back_populates="posts")


class Messages(Base):
    __tablename__ = 'messages'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    message: Mapped[str] = mapped_column(TEXT, nullable=False)
    user: Mapped[str] = mapped_column(String(50), nullable=False)
