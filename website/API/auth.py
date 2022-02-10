from flask import jsonify, Blueprint, request, make_response
from website.database.DB import SessionFactory
from website.database.models import User
from werkzeug.security import check_password_hash


api_auth = Blueprint('api_auth', __name__)


@api_auth.route('/login')
def api_login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response({'message': 'Invalid credentials!'},
                             {'www-Authenticate': 'Basic Realm="Login Required"'}), 401
    user = SessionFactory.session.query(User).filter_by(username=auth.username).first()

    if user and check_password_hash(user.password, auth.password):
        token = user.get_token()
        return jsonify({'token': token}), 200

    return make_response({'message': 'Could not verify!'},
                         {'www-Authenticate': 'Basic Realm="Login Required"'}), 401
