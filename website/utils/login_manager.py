from flask import g, request, jsonify
from functools import wraps
from flask.sessions import SecureCookieSessionInterface
from flask_login import LoginManager
from website.database.DB import SessionFactory
from website.database.models import User


class CustomCookieSessionInterface(SecureCookieSessionInterface):
    def save_session(self, app, session, response):
        if g.get('login_via_header'):
            return
        return super(CustomCookieSessionInterface, self).save_session(app, session, response)


login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'


@login_manager.user_loader
def load_user(user_id):
    return SessionFactory.session.query(User).get(int(user_id))


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.headers.get('api_key')
        if api_key:
            user = User.verify_token(api_key)
            if user:
                return f(user, *args, **kwargs)
            else:
                return jsonify({'message': 'Token expired!'}), 401
        else:
            return jsonify({'message': 'Invalid or missing token'}), 401

    return decorated
