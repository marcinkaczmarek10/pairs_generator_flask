from flask import Blueprint, render_template, flash, redirect, request
from flask_login import current_user, login_user, logout_user
from website.forms.Login import LoginForm
from website.forms.Registration import RegistrationForm
from website.DB import session
from website.models import User
from werkzeug.security import generate_password_hash, check_password_hash


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:

        return redirect('/')

    form = LoginForm()

    if form.validate_on_submit():
        user = session.query(User).filter_by(email=form.email.data).first()

        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            redirect_page = request.args.get('next')
            flash('You have been logged in', 'success')

            return redirect(redirect_page) if redirect_page else redirect('/')

        else:
            flash('Login unsuccessful', 'danger')

    return render_template(
        'login.html',
        title='Login',
        form=form
    )


@auth.route('/logout')
def logout():
    logout_user()
    return redirect('/')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:

        return redirect('/')

    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(
            form.password.data,
            method='sha256'
        )
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password
        )

        with session:
            try:
                session.add(user)
                session.commit()
            except Exception as error:
                session.rollback()
                print(error)
                raise error
            finally:
                session.close()

        flash(f'Account created {form.username.data}!', 'success')

        return redirect('login')

    return render_template(
        'register.html',
        title='Register',
        form=form
    )
