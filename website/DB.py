from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    'sqlite:///generatePairsDB.db',
    connect_args={"check_same_thread": False}
)
Session = sessionmaker(engine, expire_on_commit=False)
Base = declarative_base()
session = Session()
