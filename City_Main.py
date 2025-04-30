from fastapi import FastAPI, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List

from City_Database import SessionLocal, init_db
from City_Schemas import CityCreate, CityOut
from City_Crud import (
    get_city, get_cities, create_city,
    update_city, delete_city,
    get_cities_by_population, get_cities_by_area
)
from City_Models import City


app = FastAPI(title="City Info Service")

# Inizializza DB
init_db()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- CRUD Endpoints ---
@app.post("/cities/", response_model=CityOut)
def create(city: CityCreate, db: Session = Depends(get_db)):
    return create_city(db, city)

@app.get("/cities/", response_model=List[CityOut])
def read_all(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_cities(db, skip, limit)

@app.get("/cities/{city_id}", response_model=CityOut)
def read_one(city_id: int, db: Session = Depends(get_db)):
    city = get_city(db, city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city

@app.put("/cities/{city_id}", response_model=CityOut)
def update(city_id: int, city_data: CityCreate, db: Session = Depends(get_db)):
    db_city = get_city(db, city_id)
    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")
    return update_city(db, db_city, city_data)

@app.delete("/cities/{city_id}")
def delete(city_id: int, db: Session = Depends(get_db)):
    db_city = get_city(db, city_id)
    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")
    delete_city(db, db_city)
    return {"detail": "City deleted"}

# --- Statistic Endpoints ---
@app.get("/cities/statistics/population", response_model=List[CityOut])
def by_population(minPopulation: int = 0, maxPopulation: int = 1_000_000_000, db: Session = Depends(get_db)):
    return get_cities_by_population(db, minPopulation, maxPopulation)

@app.get("/cities/statistics/area", response_model=List[CityOut])
def by_area(minArea: float = 0.0, maxArea: float = 1_000_000.0, db: Session = Depends(get_db)):
    return get_cities_by_area(db, minArea, maxArea)
