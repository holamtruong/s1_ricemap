""" Define database connection using SQLAlchemy """

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:14031993@localhost:5432/s1_ricemap'


engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# The declarative_base() base class contains a MetaData object for tabl
Base = declarative_base()






