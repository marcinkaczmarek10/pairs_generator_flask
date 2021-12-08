from flask import Flask
from website.utils.login_manager import login_manager
from website.config import DevelopConfig
from website.utils.email import mail
from website.utils.data_serializers import marshmallow


def create_app(config_name=DevelopConfig):
    app = Flask(__name__)
    app.config.from_object(config_name)
    login_manager.init_app(app)
    mail.init_app(app)
    marshmallow.init_app(app)

    from website.auth.routes import auth
    from website.generate_pairs.routes import generate_pairs
    from website.main.routes import main
    from website.errors.error_handlers import errors
    from website.API.generate_pairs import api

    app.register_blueprint(auth)
    app.register_blueprint(generate_pairs)
    app.register_blueprint(main)
    app.register_blueprint(errors)
    app.register_blueprint(api, url_prefix='/api/')

    return app
