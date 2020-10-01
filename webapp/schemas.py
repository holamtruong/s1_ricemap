""" Pydantic models """
from typing import List, Optional
from pydantic import BaseModel
from datetime import date


# defining objects in Pydantic is via models that inherit from BaseModel
class RiceAgeStatistic(BaseModel):
    id: int
    maxa: str
    tenxa: str
    sum: float
    rice_age: str
    date: date

    class Config:
        orm_mode = True
        # taking data out of ORM, making it into a dictionary automatically
