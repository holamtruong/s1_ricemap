""" bring all the modular components together  """
from typing import List

import uvicorn

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

# from . import models, schemas
# from .database import SessionLocal, engine

from webapp import models, schemas, crud
from webapp.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Cross-Origin Resource Sharing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


# Any route use SessionLocal database connection when needed and closed after use.
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


# Root
@app.get("/")
def root():
    return RedirectResponse(url="/docs/")


# Get all data of Rice Age Statistic
@app.get("/data_stats/", response_model=List[schemas.RiceAgeStatistic])
def get_all_data(db: Session = Depends(get_db)):
    data = crud.get_all_data(db)
    return data

# Get data by rice age group
@app.get("/data_stats_riceage/{rice_age}", response_model=List[schemas.RiceAgeStatistic])
def get_data_by_rice_age(rice_age: str, db: Session = Depends(get_db)):
    data = crud.get_data_by_rice_age(db, rice_age=rice_age)
    if data is None:
        raise HTTPException(status_code=404, detail="Data not found")
    return data

# Get data by rice by maxa
@app.get("/data_stats_maxa/{maxa}", response_model=List[schemas.RiceAgeStatistic])
def get_data_by_maxa(maxa: str, db: Session = Depends(get_db)):
    data = crud.get_data_by_maxa(db, maxa=maxa)
    if data is None:
        raise HTTPException(status_code=404, detail="Data not found")
    return data





# Run app
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=3979)

'''
    
# Run on terminal:  
(venv) E:\DEV\s1_ricemap>uvicorn webapp.main:app --reload

'''
