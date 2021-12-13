from flask_marshmallow import Marshmallow
from website.database.models import RandomPair, RandomPerson


marshmallow = Marshmallow()


class ResultSchema(marshmallow.SQLAlchemyAutoSchema):
    class Meta:
        model = RandomPair
        include_fk = True


class RandomPersonSchema(marshmallow.SQLAlchemyAutoSchema):
    class Meta:
        model = RandomPerson
        include_fk = True
