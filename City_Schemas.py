from pydantic import BaseModel
from datetime import date

class CityCreate(BaseModel):
    name: str
    country: str
    population: int
    area: float
    last_census_date: date

class CityOut(CityCreate):
    id: int

    class Config:
        orm_mode = True
