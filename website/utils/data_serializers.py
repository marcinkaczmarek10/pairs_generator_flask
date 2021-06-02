from website.database.DB import SessionFactory
from website.database.models import RandomPairsResults
from flask_login import current_user

def data_serializer():
    user_random_pairs_result = SessionFactory.session.query(
        RandomPairsResults).filter_by(user_id=current_user.id).all()

    flat_results = [result.results for result in user_random_pairs_result]
    print(user_random_pairs_result)
    print(type(user_random_pairs_result))
    flatter_results = user_random_pairs_result.strip('][').split(', ')
    print(flatter_results)

data_serializer()