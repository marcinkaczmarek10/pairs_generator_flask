from flask import Blueprint, render_template, flash, redirect, request, jsonify
from flask_login import current_user, login_required
from website.forms.GenerateRandomPairs import GenerateRandomPairsForm
from website.database.DB import session
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

        with session:
            try:
                session.add(random_person)
                session.commit()
            except Exception as err:
                session.rollback()
                print(err)
            finally:
                session.close()

        return redirect('/generate-pairs')

    user_pair = session.query(
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
    pair = session.query(
        RandomPairs).filter_by(user_id=current_user.id).order_by(RandomPairs.id.desc()).first()

    if pair:
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

    flash('There is no pairs!', 'danger')
    return redirect('/generate-pairs')


@generate_pairs.route('/results', methods=['POST'])
@login_required
def results():
    user_random_person_pool = session.query(
        RandomPairs).filter_by(user_id=current_user.id).all()

    if len(user_random_person_pool) != 0 and len(user_random_person_pool) > 1:
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

        with session:
            try:
                session.add(user_random_pairs)
                session.query(RandomPairs).filter_by(user_id=current_user.id).delete()
                session.commit()
            except Exception as err:
                session.rollback()
                print(err)
            finally:
                session.close()

        return redirect('/show-results')

    flash('Add your pairs!', 'danger')
    return redirect('/generate-pairs')


@generate_pairs.route('/show-results')
@login_required
def show_results():
    user_random_pairs_result = session.query(
        RandomPairsResults).filter_by(user_id=current_user.id).all()
    flat_results = [result for result in user_random_pairs_result]
    print(flat_results)
    print(user_random_pairs_result)
    # TODO ogarnąć dostęp do tych list (results)

    return render_template(
        'results.html',
        user_random_pairs_result=user_random_pairs_result
    )


@generate_pairs.route('/delete-result', methods=['POST'])
@login_required
def delete_result():
    result_to_delete = json.loads(request.data)
    result_id = result_to_delete['result_id']
    result_query = session.query(RandomPairsResults).get(result_id)

    if result_query:
        if result_query.user_id == current_user.id:
            with session:
                try:
                    session.delete(result_query)
                    session.commit()
                except Exception as err:
                    session.rollback()
                    print(err)
                finally:
                    session.close()

            return jsonify({})
