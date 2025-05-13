from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import date, datetime

from app.core.database import get_db
from app.services.auth import get_current_doctor
from app.services.user import create_doctor, get_doctors, get_doctor
from app.services.booking import get_bookings_by_doctor, get_doctor_bookings_by_date
from app.schemas.user import DoctorCreate, DoctorResponse
from app.schemas.booking import BookingDetailResponse
from app.models.user import User

router = APIRouter(prefix="/doctors", tags=["doctors"])

@router.post("/signup", response_model=DoctorResponse, status_code=status.HTTP_201_CREATED)
def doctor_signup(doctor: DoctorCreate, db: Session = Depends(get_db)):
    return create_doctor(db=db, doctor=doctor)

@router.get("/", response_model=List[DoctorResponse])
def read_doctors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    doctors = get_doctors(db, skip=skip, limit=limit)
    return doctors

@router.get("/me", response_model=DoctorResponse)
def read_doctor_me(current_user: User = Depends(get_current_doctor)):
    return current_user

@router.get("/{doctor_id}", response_model=DoctorResponse)
def read_doctor(doctor_id: int, db: Session = Depends(get_db)):
    return get_doctor(db, doctor_id=doctor_id)

@router.get("/me/bookings", response_model=List[BookingDetailResponse])
def read_doctor_bookings(
    current_user: User = Depends(get_current_doctor),
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    bookings = get_bookings_by_doctor(db, doctor_id=current_user.id, skip=skip, limit=limit)
    return bookings

@router.get("/me/bookings/date", response_model=List[BookingDetailResponse])
def read_doctor_bookings_by_date(
    date_str: str = Query(..., description="Date in format YYYY-MM-DD"),
    current_user: User = Depends(get_current_doctor),
    db: Session = Depends(get_db)
):
    try:
        booking_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid date format. Use YYYY-MM-DD"
        )
    
    booking_datetime = datetime.combine(booking_date, datetime.min.time())
    bookings = get_doctor_bookings_by_date(db, doctor_id=current_user.id, date=booking_datetime)
    return bookings 