#from . import api
import json
from flask import jsonify, url_for
from website.database.DB import session
from website.database.models import RandomPairsResults, RandomPairs
from flask import Blueprint

api = Blueprint('api', __name__)

@api.route('/results/<user_id>')
def get_results(user_id):
    query = session.query(RandomPairsResults).filter_by(user_id=user_id).all()
    results = []
    for each in query:
        results.append(each.results)
    #results_str = [str(result) for result in results]
    results_serialized = json.dumps(results)
    #user_pairs = url_for(get_user_pairs)
    print(results_serialized)
    return jsonify({
        'results': results_serialized,
        #'user_pairs': user_pairs
    })


@api.route('/pairs/<user_id>')
def get_user_pairs(user_id):
    pass
