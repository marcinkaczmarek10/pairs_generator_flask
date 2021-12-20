import json
import itertools
import operator
from flask import Blueprint, render_template, flash, redirect, request, jsonify, abort
from flask_login import current_user, login_required
from website.database.DB import SessionFactory, SessionContextManager
from website.database.models import UsersPerson, RandomPair, DrawCount, WhichDraw
from website.generate_pairs.generate_random_pairs import Person, generate_random_pairs
from website.utils.email_sending import send_mail_to_pairs, MailError
from website.utils.data_serializers import ResultSchema
from website.utils.forms import SubmitSendingEmailForm, GenerateRandomPairsForm


generate_pairs = Blueprint('generate_pairs', __name__)


@generate_pairs.route('/generate-pairs', methods=['GET', 'POST'])
@login_required
def pairs():
    form = GenerateRandomPairsForm()

    if form.validate_on_submit():
        person = UsersPerson(
            person_name=form.person_name.data,
            person_email=form.person_email.data,
            user_id=current_user.id
        )

        with SessionContextManager() as session:
            session.add(person)

        return redirect('/generate-pairs')

    user_draw_pool = SessionFactory.session.query(UsersPerson).\
        filter_by(user_id=current_user.id).all()

    return render_template(
        'generate_pairs.html',
        title='Generate random pairs',
        form=form,
        user_pair=user_draw_pool
    )


@generate_pairs.route('/delete-person', methods=['POST'])
@login_required
def delete_person():
    person = SessionFactory.session.query(UsersPerson).\
        filter_by(user_id=current_user.id).order_by(UsersPerson.id.desc()).first()

    if person:
        with SessionContextManager() as sessionCM:
            sessionCM.delete(person)

        return redirect('/generate-pairs')

    flash('There is no person to delete!', 'danger')
    return redirect('/generate-pairs')


@generate_pairs.route('/results', methods=['POST'])
@login_required
def results():
    user_draw_pool = SessionFactory.session.query(UsersPerson).\
        filter_by(user_id=current_user.id).all()

    if len(user_draw_pool) > 1:
        draw_pool = [
            Person(row.person_name, row.person_email) for row in user_draw_pool
        ]
        user_results = generate_random_pairs(draw_pool)
        draw_count = DrawCount(user_id=current_user.id)

        with SessionContextManager() as sessionCM:
            sessionCM.add(draw_count)

        is_draw_count = SessionFactory.session.query(DrawCount).\
            filter_by(user_id=current_user.id).order_by(DrawCount.id.desc()).first()
        if is_draw_count:
            for [first_person, second_person] in user_results:
                user_random_pair = RandomPair(
                    first_person_name=first_person.name,
                    first_person_email=first_person.email,
                    second_person_name=second_person.name,
                    second_person_email=second_person.email,
                    draw_count=is_draw_count.id
                )
                with SessionContextManager() as sessionCM:
                    sessionCM.add(user_random_pair)

        with SessionContextManager():
            SessionFactory.session.query(UsersPerson).filter_by(user_id=current_user.id).delete()

        return redirect('/show-results')

    flash('Add your pairs!', 'danger')
    return redirect('/generate-pairs')


@generate_pairs.route('/show-results')
@login_required
def show_results():
    user_random_pairs_result = SessionFactory.session.query(RandomPair).\
        outerjoin(DrawCount, RandomPair.draw_count == DrawCount.id).\
        filter(DrawCount.user_id == current_user.id).all()

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
@login_required
def delete_result():
    req = request.get_data().decode('utf-8')
    result_to_delete = json.loads(req)

    if result_to_delete:
        for result_id in result_to_delete:
            result = SessionFactory.session.query(RandomPair).get(result_id['id'])
            with SessionContextManager() as sessionCM:
                sessionCM.delete(result)

    return jsonify({}), 200


@generate_pairs.route('/submit-result', methods=['POST'])
@login_required
def submit_result():
    req_json = request.get_data().decode('utf-8')
    req = json.loads(req_json)
    item_getter = operator.itemgetter('draw_count')
    draw_id = list(set(map(item_getter, req)))
    is_draw_id = SessionFactory.session.query(WhichDraw).filter_by(draw_count=draw_id[0]).first()
    if is_draw_id:

        return abort(403, description='You cannot do this')

    with SessionContextManager() as session:
        session.add(WhichDraw(draw_count=draw_id[0]))

    return jsonify({'message': 'ok'}), 200


@generate_pairs.route('/submit-sending-email', methods=['GET', 'POST'])
@login_required
def submit_sending_emails():
    form = SubmitSendingEmailForm()
    is_draw = SessionFactory.session.query(WhichDraw).\
        outerjoin(DrawCount, WhichDraw.draw_count == DrawCount.id).\
        filter(DrawCount.user_id == current_user.id).order_by(WhichDraw.id.desc()).all()
    if not is_draw:
        return redirect('/')
    if len(is_draw) > 1:
        for draw in is_draw:
            with SessionContextManager() as session:
                session.delete(draw)
        flash('More than one draw!', 'danger')
        return redirect('/show-results')
    get_count_id = is_draw[0]
    query = SessionFactory.session.query(RandomPair).filter_by(draw_count=get_count_id.draw_count).all()
    schema = ResultSchema(many=True)
    recipients = schema.dump(query)
    if form.validate_on_submit() and recipients:
        try:
            send_mail_to_pairs(recipients, form.email_title.data, form.email_body.data)
            with SessionContextManager() as session:
                session.delete(get_count_id)
            flash('Emails have been sent!', 'info')
            return redirect('/')
        except MailError:
            flash('Something went wrong!', 'danger')

    if not recipients:
        flash('There is no results', 'danger')

    return render_template('submit_sending_email.html', form=form)
