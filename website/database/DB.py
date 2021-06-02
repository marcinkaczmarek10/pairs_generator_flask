import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class ConnectionWithDataBaseError(Exception):
    pass


class NoTableFoundError(Exception):
    pass


class SessionFactory:
    database_uri = os.environ.get('DATABASE_URI')
    engine = create_engine(
        'sqlite:///generatePairsDB.db',
        connect_args={"check_same_thread": False}
    )
    Session = sessionmaker(bind=engine, expire_on_commit=False)
    Base = declarative_base()
    session = Session()


class SessionContextManager:
    def __init__(self, session=SessionFactory.session, ):
        self.session = session

    def __enter__(self):
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.session.commit()
        except Exception as err:
            self.session.rollback()
            raise err
        finally:
            self.session.close()
