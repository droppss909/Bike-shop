from fastapi import APIRouter

from fastapi import Depends
from database.database import get_db
from sqlalchemy.orm import Session
from fastapi import HTTPException
from services.schema import ServiceModel, AppointmentModel
from services.model import Service, Appointments
from services.service import get_services, get_service, post_service, delete_service, update_service, get_appointments, get_appointment, post_appointment

router = APIRouter(prefix="/services", tags=["services"])

@router.get("/", response_model=list[ServiceModel])
def get_list_services(db: Session = Depends(get_db)):
    return get_services(db)

@router.get("/{id}")
def get_service_router(id: int, db: Session = Depends(get_db)):
    return get_service(id, db)

@router.post("/")
def post_service_router(db: Session = Depends(get_db)):
    return post_service(db)

@router.delete("/{id}")
def delete_service_router(id: int, db: Session = Depends(get_db)):
    return delete_service(id, db)

@router.put("/{id}")
def update_service_router(id: int, service_data: dict, db: Session = Depends(get_db)):
    return update_service(id, service_data, db)

@router.get("/appointment/", response_model=list[AppointmentModel])
def get_list_appointments(db: Session = Depends(get_db)):
    return get_appointments(db)

@router.get("/appointment/{id}", response_model=AppointmentModel)
def get_appointment_router(id: int, db: Session = Depends(get_db)):
    return get_appointment(id, db)

@router.post("/appointment")
def post_appointment_router(appointment: AppointmentModel, db: Session = Depends(get_db)):
    return post_appointment(appointment, db)