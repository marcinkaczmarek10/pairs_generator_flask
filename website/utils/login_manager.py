from flask_login import LoginManager
from website.database.DB import SessionFactory
from website.database.models import User


login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'


@login_manager.user_loader
def load_user(user_id):
    return SessionFactory.session.query(User).get(int(user_id))
