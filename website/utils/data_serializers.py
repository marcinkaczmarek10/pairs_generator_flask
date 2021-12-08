from flask_marshmallow import Marshmallow
from website.database.models import RandomPair


marshmallow = Marshmallow()


class ResultSchema(marshmallow.SQLAlchemyAutoSchema):
    class Meta:
        model = RandomPair
        include_fk = True







      #  fields = (
     #       'id', 'first_person_name', 'first_person_email',
      #      'second_person_email', 'second_person_email', 'draw_count'
       # )
