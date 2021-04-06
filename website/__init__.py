from flask import Flask


app = Flask(__name__)


def create_app():
    app.config['SECRET_KEY'] = '9c5ac8693843f7eed9732e2db1758723'

    from .views import views

    app.register_blueprint(views)
    return app
