import json
import itertools
import operator
from flask import Blueprint, render_template, flash, redirect, request, jsonify
from flask_login import current_user, login_required
from website.forms.GenerateRandomPairs import GenerateRandomPairsForm
from website.database.DB import SessionFactory, SessionContextManager
from website.database.models import RandomPerson, RandomPair, DrawCount
from website.generate_pairs.generate_random_pairs import Person, generate_random_pairs
from website.utils.email import send_mail_to_pairs, MailError
from website.utils.data_serializers import ResultSchema


generate_pairs = Blueprint('generate_pairs', __name__)


@generate_pairs.route('/generate-pairs', methods=['GET', 'POST'])
@login_required
def pairs():
    form = GenerateRandomPairsForm()

    if form.validate_on_submit():
        random_person = RandomPerson(
            random_person_name=form.random_person_name.data,
            random_person_email=form.random_person_email.data,
            user_id=current_user.id
        )

        with SessionContextManager() as sessionCM:
            sessionCM.add(random_person)

        return redirect('/generate-pairs')

    user_pair = SessionFactory.session.query(
        RandomPerson).filter_by(user_id=current_user.id).all()

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
        RandomPerson).filter_by(user_id=current_user.id).order_by(RandomPerson.id.desc()).first()

    if pair:
        with SessionContextManager() as sessionCM:
            sessionCM.delete(pair)

        return redirect('/generate-pairs')

    flash('There is no pairs!', 'danger')
    return redirect('/generate-pairs')


@generate_pairs.route('/results', methods=['POST'])
@login_required
def results():
    user_random_person_pool = SessionFactory.session.query(
        RandomPerson).filter_by(user_id=current_user.id).all()

    if len(user_random_person_pool) > 1:
        random_person_pool = []

        for row in user_random_person_pool:
            random_person_pool.append(
                Person(row.random_person_name, row.random_person_email)
            )

        user_results = generate_random_pairs(random_person_pool)
        draw_count = DrawCount(user_id=current_user.id)

        with SessionContextManager() as sessionCM:
            sessionCM.add(draw_count)

        is_draw_count = SessionFactory.session.query(
                    DrawCount).filter_by(user_id=current_user.id).order_by(DrawCount.id.desc()).first()
        if is_draw_count:
            for [first_person, second_person] in user_results:
                user_random_pairs = RandomPair(
                    first_person_name=first_person.name,
                    first_person_email=first_person.email,
                    second_person_name=second_person.name,
                    second_person_email=second_person.email,
                    draw_count=is_draw_count.id
                )
                with SessionContextManager() as sessionCM:
                    sessionCM.add(user_random_pairs)

        SessionFactory.session.query(RandomPerson).filter_by(user_id=current_user.id).delete()

        return redirect('/show-results')

    flash('Add your pairs!', 'danger')
    return redirect('/generate-pairs')


@generate_pairs.route('/show-results')
@login_required
def show_results():
    user_random_pairs_result = SessionFactory.session.query(
        RandomPair).outerjoin(
        DrawCount, RandomPair.draw_count == DrawCount.id).filter(
        DrawCount.user_id == current_user.id).all()

    schema = ResultSchema(many=True)
    pretty_result = schema.dump(user_random_pairs_result)
    item_getter = operator.itemgetter('draw_count')
    sorted_pretty_result = sorted(pretty_result, key=item_getter)
    grouped_result = [list(g) for k, g in itertools.groupby(sorted_pretty_result, item_getter)]

    return render_template(
        'results.html',
        result=grouped_result
    )


@generate_pairs.route('/delete-result', methods=['POST'])
def delete_result():
    req = request.get_data().decode('utf-8')
    req_json = json.loads(req)

    if req_json:
        for result in req_json:
            result_query = SessionFactory.session.query(RandomPair).get(result['id'])
            print(result_query)
            with SessionContextManager() as sessionCM:
                sessionCM.delete(result_query)

    return jsonify({}, 200)


@generate_pairs.route('/submit-result', methods=['POST'])
def submit_result():
    req = request.get_data().decode('utf-8')
    req_json = json.loads(req)
    try:
        send_mail_to_pairs(req_json)
        flash('Emails have been sent!', 'info')
    except MailError:
        flash('Something went wrong!', 'danger')

    return jsonify({}, 200)
