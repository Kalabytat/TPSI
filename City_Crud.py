from sqlalchemy.orm import Session
from City_Models import City
from City_Schemas import CityCreate

def get_city(db: Session, city_id: int):
    return db.query(City).get(city_id)

def get_cities(db: Session, skip: int = 0, limit: int = 100):
    return db.query(City).offset(skip).limit(limit).all()

def create_city(db: Session, city: CityCreate):
    db_city = City(**city.dict())
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city

def update_city(db: Session, db_city: City, city_data: CityCreate):
    for attr, value in city_data.dict().items():
        setattr(db_city, attr, value)
    db.commit()
    db.refresh(db_city)
    return db_city

def delete_city(db: Session, db_city: City):
    db.delete(db_city)
    db.commit()

def get_cities_by_population(db: Session, min_pop: int, max_pop: int):
    return db.query(City).filter(City.population.between(min_pop, max_pop)).all()

def get_cities_by_area(db: Session, min_area: float, max_area: float):
    return db.query(City).filter(City.area.between(min_area, max_area)).all()
