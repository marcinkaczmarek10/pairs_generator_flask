import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


database_uri = os.environ.get('DATABASE_URI')
engine = create_engine(
    'sqlite:///generatePairsDB.db',
    connect_args={"check_same_thread": False}
)
Session = sessionmaker(bind=engine, expire_on_commit=False)
Base = declarative_base()
session = Session()