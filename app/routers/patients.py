from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.core.database import get_db
from app.services.auth import get_current_patient
from app.services.user import create_patient
from app.services.booking import get_bookings_by_patient
from app.schemas.user import PatientCreate, PatientResponse
from app.schemas.booking import BookingDetailResponse, BookingStatus
from app.models.user import User

router = APIRouter(prefix="/patients", tags=["patients"])

@router.post("/signup", response_model=PatientResponse, status_code=status.HTTP_201_CREATED)
def patient_signup(patient: PatientCreate, db: Session = Depends(get_db)):
    return create_patient(db=db, patient=patient)

@router.get("/me", response_model=PatientResponse)
def read_patient_me(current_user: User = Depends(get_current_patient)):
    return current_user

@router.get("/me/bookings", response_model=List[BookingDetailResponse])
def read_patient_bookings(
    current_user: User = Depends(get_current_patient),
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    bookings = get_bookings_by_patient(db, patient_id=current_user.id, skip=skip, limit=limit)
    return bookings

@router.get("/me/bookings/upcoming", response_model=List[BookingDetailResponse])
def read_patient_upcoming_bookings(
    current_user: User = Depends(get_current_patient),
    db: Session = Depends(get_db)
):
    all_bookings = get_bookings_by_patient(db, patient_id=current_user.id)
    now = datetime.utcnow()
    upcoming_bookings = [
        booking for booking in all_bookings 
        if booking.booking_time > now and booking.status != BookingStatus.CANCELLED
    ]
    return upcoming_bookings

@router.get("/me/bookings/past", response_model=List[BookingDetailResponse])
def read_patient_past_bookings(
    current_user: User = Depends(get_current_patient),
    db: Session = Depends(get_db)
):
    all_bookings = get_bookings_by_patient(db, patient_id=current_user.id)
    now = datetime.utcnow()
    past_bookings = [
        booking for booking in all_bookings 
        if booking.booking_time < now or booking.status == BookingStatus.COMPLETED
    ]
    return past_bookings 