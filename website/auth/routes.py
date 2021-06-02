from flask import Blueprint, render_template, flash, redirect, request
from flask_login import current_user, login_user, logout_user
from website.forms.Login import LoginForm
from website.forms.Registration import RegistrationForm
from website.forms.reset_password import ResetPasswordForm, ResetPasswordSubmitForm
from website.database.DB import SessionContextManager, SessionFactory
from website.database.models import User
from website.utils.email import send_reset_password_mail, send_verifiaction_mail
from werkzeug.security import generate_password_hash, check_password_hash


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:

        return redirect('/')

    form = LoginForm()

    if form.validate_on_submit():
        user = SessionFactory.session.query(User).filter_by(email=form.email.data).first()

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

        with SessionContextManager() as sessionCM:
            user = User(
                username=form.username.data,
                email=form.email.data,
                password=hashed_password
            )
            try:
                sessionCM.add(user)
            except Exception as err:
                flash('Nie dodało', 'danger')
                raise err

        send_verifiaction_mail(user)
        flash(
            f'Account created {form.username.data}! Confirmation link was sent to your email.',
            'success'
        )

        return redirect('login')

    return render_template(
        'register.html',
        title='Register',
        form=form
    )


@auth.route('/reset-password', methods=['GET', 'POST'])
def reset_password_submit():
    if current_user.is_authenticated:
        return redirect('/')
    form = ResetPasswordSubmitForm()
    if form.validate_on_submit():
        verified_user = SessionFactory.session.query(User).filter_by(email=form.email.data).first()
        if verified_user is None:
            flash('no user', 'danger')
        send_reset_password_mail(verified_user)
        flash('Reset link sent to your email', 'success')
        return redirect('/login')
    return render_template(
        'reset_password_submit.html',
        title='Reset_password_submit',
        form=form
    )


@auth.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect('/')

    verified_user = User.verify_token(token)
    if not verified_user:
        flash('blank', 'danger')
        return redirect('/reset-password')
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(
            form.password.data,
            method='sha256'
        )
        user_new_password = {
            User.password: hashed_password
        }
        with SessionContextManager as sessionCM:
            sessionCM.query(
                User).filter_by(id=verified_user).update(user_new_password)
        flash('Password Updated!', 'success')
        return redirect('/login')

    return render_template(
        'reset_password.html',
        title='Reset Password',
        form=form
    )


@auth.route('/confirm-email/<token>', methods=['GET', 'POST'])
def confirm_email(token):
    verified_user = User.verify_token(token)
    if User.is_confirmed is True:
        flash('Your email is already confirmed', 'info')
        return redirect('/')

    if verified_user:
        with SessionContextManager() as sessionCM:
            sessionCM.query(User).filter_by(id=verified_user).update(User.is_confirmed is True)
            flash('Your email has been confirmed.', 'info')
            return redirect('/login')

    return render_template('confirm_email.html')
