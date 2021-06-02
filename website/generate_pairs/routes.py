from flask import Blueprint, render_template, flash, redirect, request, jsonify
from flask_login import current_user, login_required
from website.forms.GenerateRandomPairs import GenerateRandomPairsForm
from website.database.DB import SessionFactory, SessionContextManager
from website.database.models import RandomPairs, RandomPairsResults
from website.generate_pairs.generate_random_pairs import RandomPerson, generate_random_pairs
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

        with SessionContextManager() as sessionCM:
            sessionCM.add(random_person)

        return redirect('/generate-pairs')

    user_pair = SessionFactory.session.query(
        RandomPairs).filter_by(user_id=current_user.id).all()

    return render_template(
        'generate_pairs.html',
        title='Generate random pairs',
        form=form,
        user_pair=user_pair
    )


@generate_pairs.route('/delete-pair', methods=['POST'])
@login_required
def delete_pair():
    pair = SessionFactory.session.query(
        RandomPairs).filter_by(user_id=current_user.id).order_by(RandomPairs.id.desc()).first()

    if pair:
        with SessionContextManager as sessionCM:
            sessionCM.delete(pair)

        return redirect('/generate-pairs')

    flash('There is no pairs!', 'danger')
    return redirect('/generate-pairs')


@generate_pairs.route('/results', methods=['POST'])
@login_required
def results():
    user_random_person_pool = SessionFactory.session.query(
        RandomPairs).filter_by(user_id=current_user.id).all()

    if len(user_random_person_pool) > 1:
        random_person_pool = []

        for row in user_random_person_pool:
            random_person_pool.append(
                RandomPerson(row.random_person_name, row.random_person_email)
            )

        user_results = generate_random_pairs(random_person_pool)
        user_random_pairs = RandomPairsResults(
            results=user_results,
            user_id=current_user.id
        )

        with SessionContextManager() as sessionCM:
            sessionCM.add(user_random_pairs)
            SessionFactory.session.query(RandomPairs).filter_by(user_id=current_user.id).delete()

        return redirect('/show-results')

    flash('Add your pairs!', 'danger')
    return redirect('/generate-pairs')


@generate_pairs.route('/show-results')
@login_required
def show_results():
    user_random_pairs_result = SessionFactory.session.query(
        RandomPairsResults).filter_by(user_id=current_user.id).all()

    flat_results = [result.results for result in user_random_pairs_result]
    print(user_random_pairs_result)
    print(type(user_random_pairs_result))
    json_results = str(flat_results)
    print(json_results)


    return render_template(
        'results.html',
        user_random_pairs_result=user_random_pairs_result
    )


@generate_pairs.route('/delete-result', methods=['POST'])
@login_required
def delete_result():
    result_to_delete = json.loads(request.data)
    result_id = result_to_delete['result_id']
    result_query = SessionFactory.session.query(RandomPairsResults).get(result_id)

    if result_query and result_query.user_id == current_user.id:
        with SessionContextManager() as sessionCM:
            sessionCM.delete(result_query)

        return jsonify({})
