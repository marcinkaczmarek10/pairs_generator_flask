from flask import Blueprint, render_template, flash, redirect, request, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from .forms import RegistrationForm, LoginForm, GenerateRandomPairsForm
from .DB import session
from . models import User, RandomPairs, RandomPairsResults
from werkzeug.security import generate_password_hash, check_password_hash
from .generate_random_pairs import generate_random_pairs, RandomPerson
import json

views = Blueprint('views', __name__)


@views.route('/')
def home_view():
    return render_template(
        'home.html',
        )


@views.route('/login', methods=['GET', 'POST'])
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


@views.route('/logout')
def logout():
    logout_user()
    return redirect('/')


@views.route('/register', methods=['GET', 'POST'])
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


@views.route('/generate-pairs', methods=['GET', 'POST'])
@login_required
def generate_pairs():
    form = GenerateRandomPairsForm()

    if form.validate_on_submit():
        random_person = RandomPairs(
            random_person_name=form.random_person_name.data,
            random_person_email=form.random_person_email.data,
            user_id=current_user.id
        )

        with session:
            try:
                session.add(random_person)
                session.commit()
            except Exception:
                session.rollback()
                raise
            finally:
                session.close()

        return redirect('/generate-pairs')

    user_pair = session.query(RandomPairs).filter_by(user_id=current_user.id).all()

    return render_template(
        'generate_pairs.html',
        title='Generate random pairs',
        form=form,
        user_pair=user_pair
    )


@views.route('/delete-pair', methods=['POST'])
@login_required
def delete_pair():
    pair = session.query(
        RandomPairs).filter_by(user_id=current_user.id).order_by(RandomPairs.id.desc()).first()

    with session:
        try:
            session.delete(pair)
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    return redirect('/generate-pairs')


@views.route('/results', methods=['GET', 'POST'])
@login_required
def results():
    user_random_person_pool = session.query(RandomPairs).filter_by(user_id=current_user.id).all()

    if len(user_random_person_pool) % 2 == 0 and len(user_random_person_pool) != 0:

        random_person_pool = []

        for row in user_random_person_pool:
            random_person_pool.append(
                RandomPerson(row.random_person_name, row.random_person_email)
            )

        def call_generate_random_pairs():
            random_pairs = generate_random_pairs(random_person_pool)
            pairs_list = []

            for [person_one, person_two] in random_pairs:
                pairs_list.append([f'{person_one.name}, {person_one.email}', f'{person_two.name}, {person_two.email}'])

            return json.dumps(pairs_list)

        execute_call_generate_random_pairs = call_generate_random_pairs()

        user_random_pairs = RandomPairsResults(
            results=execute_call_generate_random_pairs,
            user_id=current_user.id
        )

        with session:
            try:
                session.add(user_random_pairs)
                session.query(RandomPairs).filter_by(user_id=current_user.id).delete()
                session.commit()
            except Exception:
                session.rollback()
                raise
            finally:
                session.close()

        return redirect('/show-results')

    elif len(user_random_person_pool) == 0:
        flash('Add your pairs!', 'danger')

        return redirect('/generate-pairs')

    else:
        flash('The number of pairs has to be equal', 'danger')

        return redirect('/generate-pairs')


@views.route('/show-results')
@login_required
def show_results():
    user_random_pairs_result = session.query(RandomPairsResults).filter_by(user_id=current_user.id).all()

    return render_template(
        'results.html',
        user_random_pairs_result=user_random_pairs_result
    )


@views.route('/delete-result', methods=['POST'])
@login_required
def delete_result():
    result_to_delete = json.loads(request.data)
    result_id = result_to_delete.get('resultId')
    result_query = session.query(RandomPairsResults).get(result_id)

    if result_query:
        if result_query.user_id == current_user.id:
            with session:
                try:
                    session.delete(result_query)
                    session.commit()
                except Exception:
                    session.rollback()
                    raise
                finally:
                    session.close()

            return jsonify({})
