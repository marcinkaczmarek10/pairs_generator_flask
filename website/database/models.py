from website.database.DB import Base, engine
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from website.database.DB import session


class User(Base, UserMixin):
    __tablename__ = 'users'

    id = Column(
        Integer,
        primary_key=True
    )
    username = Column(
        String(20),
        unique=True,
        nullable=False
    )
    email = Column(
        String(120),
        unique=True,
        nullable=False
    )
    password = Column(
        String(60),
        nullable=False
    )
    user_pairs = relationship(
        'RandomPairs'
    )
    user_results = relationship(
        'RandomPairsResults'
    )

    def get_token(self, expires_sec=1800):
        serializer = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return serializer.dumps({
            'user_id': self.id
        }).decode('utf-8')

    @staticmethod
    def verify_token(token):
        serializer = Serializer(current_app.config['SECRET_KEY'])
        try:
            verified_user = serializer.loads(token)['user_id']
        except Exception:
            return None
        return session.query(User).get(verified_user)

    def __repr__(self):
        return f'User({self.username},{self.email})'


class RandomPairs(Base):
    __tablename__ = 'RandomPairs'

    id = Column(
        Integer,
        primary_key=True
    )
    random_person_name = Column(
        String(20),
        nullable=False
    )
    random_person_email = Column(
        String(120),
        nullable=False
    )
    user_id = Column(
        Integer,
        ForeignKey(
            'users.id'
        )
    )

    def __repr__(self):
        return f'RandomPairs({self.random_person_name}, {self.random_person_email})'


class RandomPairsResults(Base):
    __tablename__ = 'randomPairResults'

    id = Column(
        Integer,
        primary_key=True
    )
    results = Column(
        String(500),
        nullable=False
    )
    user_id = Column(
        Integer,
        ForeignKey(
            'users.id'
        )
    )

    def __repr__(self):
        return f'RandomPairsResults({self.results})'


Base.metadata.create_all(engine)
