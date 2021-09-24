from flask import jsonify, request, url_for, abort

from app.api import bp
from app.api.auth import token_auth
from app.api.errors import bad_request
from app.models import User
from app.services import get_user_by_id_or_404, get_user_dict_collection, get_user_by_username, get_user_by_email, \
    update_user_from_dict


@bp.route('/users/<int:id>', methods=['GET'])
@token_auth.login_required
def get_user(id):
    return jsonify(
        get_user_by_id_or_404(id).to_dict())


@bp.route('/users', methods=['GET'])
@token_auth.login_required
def get_users():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = get_user_dict_collection(
        query=User.query, page=page, per_page=per_page,
        endpoint='api.get_users')
    return jsonify(data)


@bp.route('/users/<int:id>/followers', methods=['GET'])
@token_auth.login_required
def get_followers(id):
    user = get_user_by_id_or_404(id)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = get_user_dict_collection(
        query=user.followers, page=page, per_page=per_page,
        endpoint='api.get_followers', id=id)
    return jsonify(data)


@bp.route('/users/<int:id>/followed', methods=['GET'])
@token_auth.login_required
def get_followed(id):
    user = get_user_by_id_or_404(id)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = get_user_dict_collection(
        query=user.followed, page=page, per_page=per_page,
        endpoint='api.get_followed', id=id)
    return jsonify(data)


@bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json() or {}
    if not all(keys in data for keys in ('username', 'email', 'password')):
        return bad_request('must include username, email, password fields')
    if get_user_by_username(username=data['username']):
        return bad_request('please use a different username')
    if get_user_by_email(email=data['email']):
        return bad_request('please use different email')

    user = update_user_from_dict(data=data, new_user=True)

    response = jsonify(user.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_user', id=user.id)
    return response


@bp.route('/users/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_user(id):
    if token_auth.current_user().id != id:
        abort(403)

    user = get_user_by_id_or_404(id)
    data = request.get_json() or {}
    if ('username' in data and
            data['username'] != user.username and
            get_user_by_username(data['username'])):
        return bad_request('please use different username')
    if ('email' in data and
            data['email'] != user.email and
            get_user_by_email(data['email'])):
        return bad_request('please use different email')

    user = update_user_from_dict(data=data, new_user=False)
    return jsonify(user.to_dict())
