from flask import Flask
from website.login_manager import login_manager


app = Flask(__name__)


def create_app():
    app.config['SECRET_KEY'] = '9c5ac8693843f7eed9732e2db1758723'
    login_manager.init_app(app)

    from website.auth.auth import auth
    from website.generate_pairs.generate_pairs import generate_pairs
    from website.main.main import main

    app.register_blueprint(auth)
    app.register_blueprint(generate_pairs)
    app.register_blueprint(main)
    return app
