from flask import Blueprint, render_template

main = Blueprint('main', __name__)


@main.route('/')
def home_view():
    return render_template(
        'home.html',
        )

@main.route('/zohoverify/verifyforzoho.html')
def zoho():
    return render_template('zoho.html')
