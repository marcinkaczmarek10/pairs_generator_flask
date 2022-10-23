import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


if os.environ.get('ENV') == 'PRODUCTION':
    database_uri = os.environ.get('DATABASE_URL')
    if database_uri.startswith('postgres://'):
        database_uri = database_uri.replace('postgres://', 'postgresql://', 1)
elif os.environ.get('ENV') == 'DEV':
    database_uri = f'postgresql://{os.environ.get("POSTGRES_USER")}:{os.environ.get("POSTGRES_PASSWORD")}@' \
        f'{os.environ.get("POSTGRES_SERVER")}:{os.environ.get("POSTGRES_PORT")}/{os.environ.get("POSTGRES_DB")}'
else:
    database_uri = 'sqlite://:memory:'


class ConnectionWithDataBaseError(Exception):
    pass


class NoTableFoundError(Exception):
    pass


class SessionFactory:
    engine = create_engine(
        database_uri # connect_args={"check_same_thread": False}
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
