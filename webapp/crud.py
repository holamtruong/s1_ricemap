from sqlalchemy.orm import Session
from webapp import models, schemas

# get_all_data
def get_all_data(db: Session):
    records = db.query(models.RiceAgeStatistic).all()
    return records


# get_data_by_rice_age
def get_data_by_rice_age(db: Session, rice_age: str):
    records = db.query(models.RiceAgeStatistic).filter(models.RiceAgeStatistic.rice_age == rice_age).all()
    return records


# get_data_by_maxa
def get_data_by_maxa(db: Session, maxa: str):
    records = db.query(models.RiceAgeStatistic).filter(models.RiceAgeStatistic.maxa == maxa).all()
    return records
