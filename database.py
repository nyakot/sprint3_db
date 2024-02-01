from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_URL = 'postgresql+psycopg2://postgres:adminadmin@localhost/marketplace'

engine = create_engine(DB_URL)
session = sessionmaker(bind=engine)
Base = declarative_base()
