from flask import Blueprint, render_template

errors = Blueprint('errors', __name__)


@errors.errorhandler(404)
def _handler_404(error):
    if error == 404:
        return render_template('errors/404.html'), 404
