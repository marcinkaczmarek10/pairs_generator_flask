from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from website.database.DB import SessionFactory


class User(SessionFactory.Base, UserMixin):
    __tablename__ = 'users'

    id = Column(
        Integer,
        primary_key=True
    )
    username = Column(
        String(40),
        unique=True,
        nullable=False
    )
    email = Column(
        String(120),
        unique=True,
        nullable=False
    )
    password = Column(
        String(100),
        nullable=False
    )
    is_confirmed = Column(
        Boolean,
        default=False
    )
    is_admin = Column(
        Boolean,
        default=False
    )
    user_pairs = relationship(
        'UsersPerson'
    )
    user_results = relationship(
        'DrawCount'
    )

    def get_token(self, expires_sec=3600):
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
        return SessionFactory.session.query(User).get(verified_user)

    def __repr__(self):
        return f'User({self.username},{self.email})'


class UsersPerson(SessionFactory.Base):
    __tablename__ = 'usersPeople'

    id = Column(
        Integer,
        primary_key=True
    )
    person_name = Column(
        String(40),
        nullable=False
    )
    person_email = Column(
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
        return f'UsersPerson({self.person_name}, {self.person_email})'


class DrawCount(SessionFactory.Base):
    __tablename__ = 'drawCounts'

    id = Column(
        Integer,
        primary_key=True
    )
    user_id = Column(
        Integer,
        ForeignKey(
            'users.id'
        )
    )
    draw_pairs = relationship(
        'RandomPair'
    )
    which_count_clicked = relationship(
        'WhichDraw',
        backref='which_draw',
        uselist=False
    )


class RandomPair(SessionFactory.Base):
    __tablename__ = 'randomPairs'

    id = Column(
        Integer,
        primary_key=True
    )
    first_person_name = Column(
        String(40),
        nullable=False
    )
    first_person_email = Column(
        String(120),
        nullable=False
    )
    second_person_name = Column(
        String(40),
        nullable=False
    )
    second_person_email = Column(
        String(120),
        nullable=False
    )
    draw_count = Column(
        Integer,
        ForeignKey(
            'drawCounts.id'
        )
    )


class WhichDraw(SessionFactory.Base):
    __tablename__ = 'whichDraws'

    id = Column(
        Integer,
        primary_key=True
    )
    draw_count = Column(
        Integer,
        ForeignKey(
            'drawCounts.id',
        ),
        unique=True
    )


SessionFactory.Base.metadata.create_all(SessionFactory.engine)
