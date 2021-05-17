from website.DB import Base, engine
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from flask_login import UserMixin


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
