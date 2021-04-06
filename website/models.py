from website.DB import Base, engine
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from website import app
from flask_login import UserMixin, LoginManager
from .DB import session

login_manager = LoginManager(app)
login_manager.login_view = 'views.login'
login_manager.login_message_category = 'info'


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


@login_manager.user_loader
def load_user(user_id):
    return session.query(User).get(int(user_id))


Base.metadata.create_all(engine)
