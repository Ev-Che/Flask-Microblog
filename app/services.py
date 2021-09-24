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


def get_user_by_id_or_404(id):
    return User.query.get_or_404(id)


def get_user_dict_collection(query, page, per_page, endpoint, **kwargs):
    return User.to_collection_dict(query=query, page=page, per_page=per_page,
                                   endpoint=endpoint, **kwargs)


def update_user_password(user: User, password: str) -> None:
    user.set_password(password)
    db.session.commit()


def add_user_to_db(username: str, email: str, password: str) -> None:
    user = User(username=username,
                email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()


def update_user_from_dict(data: dict, new_user: bool) -> User:
    user = User()
    user.from_dict(data=data, new_user=new_user)
    db.session.add(user) if new_user else None
    db.session.commit()
    return user


def rollback() -> None:
    db.session.rollback()


def commit() -> None:
    db.session.commit()


def add_post(body: str, author: User, language: str) -> None:
    post = Post(body=body, author=author, language=language)
    db.session.add(post)
    db.session.commit()


def get_post_stream():
    return Post.query.order_by(Post.timestamp.desc())


def add_obj_to_db_session(obj):
    db.session.add(obj)


def get_user_by_token(token):
    return User.query.filter_by(token=token).first()


def check_user_token(token):
    return User.check_token(token) if token else None
