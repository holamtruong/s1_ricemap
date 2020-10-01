"""  Classes are the SQLAlchemy models """
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.types import Date

#from .database import Base
from webapp.database import Base


# creates the model or schema for the table 'rice_age_statistics' in database.
class RiceAgeStatistic(Base):
    __tablename__ = "rice_age_statistics"

    id = Column(Integer, primary_key=True)
    maxa = Column(String)
    tenxa = Column(String)
    sum = Column(Float)
    rice_age = Column(String)
    date = Column(Date)


