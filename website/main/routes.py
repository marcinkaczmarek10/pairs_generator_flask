from flask import Blueprint, render_template

main = Blueprint('main', __name__)


@main.route('/')
def home_view():
    return render_template(
        'home.html',
        )
