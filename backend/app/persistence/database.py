from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base


"""
This is a helper file to initialize the SQLite database and hold the connection string
"""

SQLALCHEMY_DATABASE_URL = 'sqlite:///./persistence/ml-starter-backend.db?check_same_thread=False'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

Base = declarative_base()
