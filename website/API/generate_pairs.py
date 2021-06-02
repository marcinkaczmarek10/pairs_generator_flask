#from . import api
import json
from flask import jsonify, url_for, abort
from website.database.DB import SessionFactory, SessionContextManager
from website.database.models import RandomPairsResults, RandomPairs
from flask import Blueprint
from website.generate_pairs.generate_random_pairs import generate_random_pairs, RandomPerson

api = Blueprint('api', __name__)


@api.route('/results/<user_id>')
def get_results(user_id):
    query = SessionFactory.session.query(RandomPairsResults).filter_by(user_id=user_id).all()
    results = [each.results for each in query]
    results_serialized = json.dumps(results)
    user_pairs = url_for('api.get_user_pairs', user_id=['user_id'])

    return jsonify({
        'results': results_serialized,
        'user_pairs': user_pairs
    })


@api.route('/pairs/<user_id>')
def get_user_pairs(user_id):
    query = SessionFactory.session.query(RandomPairs).filter_by(user_id=user_id).all()
    user_pairs = []
    for pair in query:
        user_pairs.append(pair.results)
    pairs_serialized = json.dumps(user_pairs)
    generate_pairs = url_for('api.post_generate_pairs', user_id=['user_id'], user_pairs=['user_pairs'])

    return jsonify({
        'user_pairs': pairs_serialized,
        'generate pairs': generate_pairs
    })


@api.route('/generate-pairs/<user_id>', methods=['POST'])
def post_generate_pairs(user_id, user_pairs):
    user_random_people_pool = user_pairs

    if len(user_random_people_pool) > 1:

        random_people_pool = [
            RandomPerson(row.random_person_name, row.random_person_email) for row in user_random_people_pool
        ]
        user_results = generate_random_pairs(random_people_pool)
        user_random_pairs = RandomPairsResults(
            results=user_results,
            user_id=user_id
        )
        with SessionContextManager as sessionCM:
            sessionCM.add(user_random_pairs)
            sessionCM.query(RandomPairs).filter_by(user_id=user_id).delete()

        get_results_url = url_for('api.get_results', user_id=user_id)
        return jsonify({
            'get_results': get_results_url
        })

    return abort(404)


@api.route('/delete-pairs<user_id>', methods=['DELETE'])
def delete_pairs(user_id):
    pass


@api.route('/delete-results<user_id>', methods=['DELETE'])
def delete_results(user_id):
    pass


@api.route('/send-email<user_id>', methods=['POST'])
def send_email_to_chosen(user_id, results):
    pass
