from flask_marshmallow import Marshmallow
from website.database.models import RandomPair, UsersPerson


marshmallow = Marshmallow()


class ResultSchema(marshmallow.SQLAlchemyAutoSchema):
    class Meta:
        model = RandomPair
        include_fk = True


class RandomPersonSchema(marshmallow.SQLAlchemyAutoSchema):
    class Meta:
        model = UsersPerson
        include_fk = True
