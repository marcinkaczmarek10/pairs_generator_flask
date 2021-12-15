import operator
import itertools
from flask import jsonify, abort, Blueprint, request
from website.database.DB import SessionFactory, SessionContextManager
from website.database.models import RandomPerson, RandomPair, DrawCount
from website.generate_pairs.generate_random_pairs import generate_random_pairs, Person
from website.utils.data_serializers import ResultSchema, RandomPersonSchema
from website.utils.login_manager import token_required


api = Blueprint('api', __name__)


@api.route('/results/')
@token_required
def get_results(user):
    query = SessionFactory.session.query(
        RandomPair).outerjoin(
        DrawCount, RandomPair.draw_count == DrawCount.id).filter(
        DrawCount.user_id == user.id).all()

    schema = ResultSchema(many=True)
    pretty_result = schema.dump(query)
    item_getter = operator.itemgetter('draw_count')
    sorted_pretty_result = sorted(pretty_result, key=item_getter)
    grouped_result = [list(g) for k, g in itertools.groupby(sorted_pretty_result, item_getter)]

    return jsonify(grouped_result), 200


@api.route('/pairs')
@token_required
def get_user_pairs(user):
    query = SessionFactory.session.query(RandomPerson).filter_by(user_id=user.id).all()
    schema = RandomPersonSchema(many=True)
    user_pairs = schema.dump(query)

    return jsonify(user_pairs), 200


@api.route('/generate-pairs', methods=['POST'])
@token_required
def post_generate_pairs(user, user_pairs):
    user_random_people_pool = user_pairs

    if len(user_random_people_pool) > 1:
        random_person_pool = [
            Person(row.random_person_name, row.random_person_email) for row in user_random_people_pool
        ]
        user_results = generate_random_pairs(random_person_pool)
        draw_count = DrawCount(user_id=user.id)

        with SessionContextManager() as sessionCM:
            sessionCM.add(draw_count)

        is_draw_count = SessionFactory.session.query(
            DrawCount).filter_by(user_id=user.id).order_by(DrawCount.id.desc()).first()
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

        with SessionContextManager():
            SessionFactory.session.query(RandomPerson).filter_by(user_id=user.id).delete()

        return jsonify({'Message': 'Your pairs were created!'}), 200

    return abort(404)


@api.route('/delete-pair', methods=['DELETE'])
@token_required
def delete_pair(user):
    pair = request.get_json()
    pair_id = pair['pair']
    query = SessionFactory.session.query(RandomPerson).filter_by(user_id=user.id, id=pair_id).first()
    if pair and query:
        with SessionContextManager() as session:
            session.delete(query)

        return jsonify({'message': 'Pair deleted!'}), 200

    return jsonify({'message': 'There is no pair!'}), 404


@api.route('/delete-results', methods=['DELETE'])
@token_required
def delete_results(user):
    result = request.get_json()
    draw_id = result['draw_count']
    query = SessionFactory.session.query(RandomPair).filter_by(draw_count=draw_id).all()
    if query:
        with SessionContextManager() as session:
            session.delete(query)

        return jsonify({'message': 'Result deleted!'}), 200

    return jsonify({'message': 'There is no result!'}), 404


@api.route('/send-email<user_id>', methods=['POST'])
@token_required
def send_email_to_chosen(user):
    pass
