from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.core.database import get_db
from app.services.auth import get_current_patient, get_current_user, get_current_doctor
from app.services.booking import create_booking, update_booking_status, get_booking, get_available_slots
from app.schemas.booking import BookingCreate, BookingResponse, BookingDetailResponse, BookingUpdate, AvailableSlot
from app.models.user import User, UserType

router = APIRouter(prefix="/bookings", tags=["bookings"])

@router.post("/", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
def create_new_booking(
    booking: BookingCreate,
    current_user: User = Depends(get_current_patient),
    db: Session = Depends(get_db)
):
    return create_booking(db=db, booking=booking, patient_id=current_user.id)

@router.get("/{booking_id}", response_model=BookingDetailResponse)
def read_booking(
    booking_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    booking = get_booking(db, booking_id)
    
    # Check if the user has access to this booking
    if (current_user.user_type == UserType.PATIENT and booking.patient_id != current_user.id) or \
       (current_user.user_type == UserType.DOCTOR and booking.doctor_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this booking"
        )
    
    return booking

@router.put("/{booking_id}/status", response_model=BookingResponse)
def update_booking(
    booking_id: int,
    booking_update: BookingUpdate,
    current_user: User = Depends(get_current_doctor),  # Only doctors can update status
    db: Session = Depends(get_db)
):
    # Check if the booking belongs to the doctor
    booking = get_booking(db, booking_id)
    if booking.doctor_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this booking"
        )
    
    return update_booking_status(db, booking_id, booking_update)

@router.get("/doctor/{doctor_id}/available", response_model=List[AvailableSlot])
def get_doctor_available_slots(
    doctor_id: int,
    date_str: str = Query(..., description="Date in format YYYY-MM-DD"),
    current_user: User = Depends(get_current_patient),
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
    return get_available_slots(db, doctor_id, booking_datetime) 