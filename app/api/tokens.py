from flask import jsonify

from app.api import bp
from app.api.auth import basic_auth, token_auth
from app.services import commit


@bp.route('tokens', methods=['POST'])
@basic_auth.login_required
def get_token():
    token = basic_auth.current_user().get_token()
    commit()
    return jsonify({'token': token})


@bp.route('/tokens', methods=['DELETE'])
@token_auth.login_required
def revoke_token():
    token_auth.current_user().revoke_token()
    commit()
    return '', 204
