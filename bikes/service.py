from bikes.schema import BikeModel, BikeCreate
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from bikes.model import Bike
from datetime import datetime, timedelta
from sqlalchemy import select
from sqlalchemy.orm import selectinload


def get_bikes(db: Session):
    bikes = db.query(Bike).all()
    valid_bikes = [
    BikeModel(
        id=bike.id, 
        brand=bike.brand, 
        model=bike.model, 
        year=bike.year, 
        price=bike.price, 
        equipment=bike.equipment, 
        color=bike.color,
        version=bike.version
    ) 
    for bike in bikes if not(bike.price == " ") or not(bike.brand == " ")
    ]
    return valid_bikes

def get_bike(id: int, db: Session):
    try:
        bike = db.query(Bike).filter(Bike.id == id).first()
        return BikeModel(id=bike.id, brand=bike.brand, model=bike.model, year=bike.year, price=bike.price, equipment=bike.equipment, color=bike.color)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to get bike. Error: {}".format(str(e)))


def get_amount_of_bikes(page: int, amount: int, db: Session):
    if page < 1 or amount < 1:
        raise HTTPException(status_code=400, detail="Page and amount must be greater than 0")

    offset = (page - 1) * amount

    try:
        bikes = db.query(Bike).offset(offset).limit(amount).all()
        return [
            BikeModel(
                id=bike.id,
                brand=bike.brand,
                model=bike.model,
                year=bike.year,
                price=bike.price,
                equipment=bike.equipment,
                color=bike.color,
                version=bike.version
            ) for bike in bikes
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve bikes. Error: {str(e)}")

def add_bike(db: Session):
    try:
        max_id = db.query(func.max(Bike.id)).scalar()
        new_id = max_id + 1 if max_id else 1 
        db_bike = Bike(id=new_id, brand=" ", model=" ", year=" ", price=" ", equipment=" ", color=" ")
        db.add(db_bike)
        db.commit()
        db.refresh(db_bike)
        return {"id_is": new_id}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create bike. Error: {}".format(str(e)))
    
    
def delete_bike(id: int, db: Session):
    bike = db.query(Bike).filter(Bike.id == id).first()

    if not bike:
        raise HTTPException(status_code=404, detail="Bike not found")

    try:
        db.delete(bike)
        db.commit()
        return {"message": "Bike deleted successfully"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete bike. Error: {}".format(str(e)))
    
def update_bike(id: int, bike_data: dict, db: Session):
    user_provided_version = bike_data.get('version')
    
    if user_provided_version is None:
        raise HTTPException(status_code=400, detail="Version not provided")

    bike = db.query(Bike).filter(Bike.id == id).first()

    if not bike:
        raise HTTPException(status_code=404, detail="Bike not found")

    current_version = bike.version

    if user_provided_version != current_version:
        raise HTTPException(status_code=409, detail="Conflict: Bike has been updated by another transaction")

    try:
        for attr, value in bike_data.items():
            if hasattr(bike, attr) and attr != 'version':  
                setattr(bike, attr, value)


        bike.version += 1

        db.commit()
        db.refresh(bike)

        return bike
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to update bike. Error: {}".format(str(e)))