from services.schema import ServiceModel, AppointmentModel
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from services.model import Service, Appointments
from datetime import datetime, timedelta
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import List


def get_services(db: Session):
    try:
        services = db.query(Service).all()
        return [ServiceModel(name=service.name, description=service.description, price=service.price) for service in services]
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to get service. Error: {}".format(str(e))) 

def get_service(id: int, db: Session):
    try:
        service = db.query(Service).filter(Service.id == id).first()
        return service
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to create service. Error: {}".format(str(e))) 

def post_service(service: ServiceModel, db: Session):
    try:
        max_id = db.query(func.max(Service.id)).scalar()
        new_id = max_id + 1 if max_id else 1 
        db_service = Service(id=new_id, **service.dict())
        db.add(db_service)
        db.commit()
        db.refresh(db_service)
        return {"acknowledge"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create service. Error: {}".format(str(e))) 


def delete_service(id: int, db: Session):
    service = db.query(Service).filter(Service.id == id).first()

    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    try:
        db.delete(service)
        db.commit()
        return {"message": "Service deleted successfully"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete service. Error: {}".format(str(e))) 

def update_service(id: int, service_data: ServiceModel, db: Session):
    service = db.query(Service).filter(Service.id == id).first()

    if not service:
        raise HTTPException(status_code=404, detail="service not found")

    try:
        for attr, value in service_data.items():
            if hasattr(service, attr):
                setattr(service, attr, value)
        
        db.commit()
        db.refresh(service)
        
        return service
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to update service. Error: {}".format(str(e)))
    
def get_appointments(db: Session):
    try:
        appointments = db.query(Appointments).all()
        return [AppointmentModel(id=appointment.id, customer_id=appointment.customer_id, date=str(appointment.date), services=appointment.services, posted=appointment.posted) for appointment in appointments]
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to get appointment. Error: {}".format(str(e))) 


def get_appointment(id, db: Session):
    try:
        appointment = db.query(Appointments).filter(Appointments.id == id).first()
        return AppointmentModel(id=appointment.id, customer_id=appointment.customer_id, date=str(appointment.date), services=appointment.services, posted=appointment.posted)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to get appointment. Error: {}".format(str(e))) 

def post_appointment(appointment: AppointmentModel, db: Session):
    try:
        max_id = db.query(func.max(Appointments.id)).scalar()
        new_id = max_id + 1 if max_id else 1 
        db_appointment = Appointments(id=new_id, **appointment.dict(), posted=False)
        db.add(db_appointment)
        db.commit()
        db.refresh(db_appointment)
        return {"acknowledge"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create appointment. Error: {}".format(str(e))) 
