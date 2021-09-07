from sqlalchemy.orm import session
from app import db
from .models import User, Post


def get_user_by_username_or_404(username):
    return User.query.filter_by(username=username).first_or_404()


def get_user_by_username(username):
    return User.query.filter_by(username=username).first()


def get_user_by_email(email):
    return User.query.filter_by(email=email).first()


def get_user_by_id(id: int):
    return User.query.get(id)


def update_user_password(user: User, password: str) -> None:
    user.set_password(password)
    db.session.commit()


def add_user_to_db(username: str, email: str, password: str) -> None:
    user = User(username=username,
                email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()


def rollback() -> None:
    db.session.rollback()


def add_post(body: str, author: User, language: str) -> None:
    post = Post(body=body, author=author, language=language)
    db.session.add(post)
    db.session.commit()


def get_post_stream():
    return Post.query.order_by(Post.timestamp.desc())
