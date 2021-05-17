from flask import Blueprint, render_template, flash, redirect, request, jsonify
from flask_login import current_user, login_required
from website.forms.GenerateRandomPairs import GenerateRandomPairsForm
from website.DB import session
from website.models import RandomPairs, RandomPairsResults
from website.generate_pairs.generate_random_pairs import generate_random_pairs, RandomPerson
import json


generate_pairs = Blueprint('generate_pairs', __name__)


@generate_pairs.route('/generate-pairs', methods=['GET', 'POST'])
@login_required
def pairs():
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


@generate_pairs.route('/delete-pair', methods=['POST'])
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


@generate_pairs.route('/results', methods=['GET', 'POST'])
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


@generate_pairs.route('/show-results')
@login_required
def show_results():
    user_random_pairs_result = session.query(RandomPairsResults).filter_by(user_id=current_user.id).all()

    return render_template(
        'results.html',
        user_random_pairs_result=user_random_pairs_result
    )


@generate_pairs.route('/delete-result', methods=['POST'])
@login_required
def delete_result():
    result_to_delete = json.loads(request.data)
    result_id = result_to_delete.get('resultId')
    result_query = session.query(RandomPairsResults).get(result_id)

    if result_query and result_query.user_id == current_user.id:
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
