from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime, timedelta
from typing import List

from app.models.booking import Booking
from app.models.user import User, UserType
from app.schemas.booking import BookingCreate, BookingUpdate, AvailableSlot

def get_bookings_by_doctor(db: Session, doctor_id: int, skip: int = 0, limit: int = 100):
    return db.query(Booking).filter(Booking.doctor_id == doctor_id).offset(skip).limit(limit).all()

def get_bookings_by_patient(db: Session, patient_id: int, skip: int = 0, limit: int = 100):
    return db.query(Booking).filter(Booking.patient_id == patient_id).offset(skip).limit(limit).all()

def get_booking(db: Session, booking_id: int):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if booking is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
    return booking

def create_booking(db: Session, booking: BookingCreate, patient_id: int):
    # Check if doctor exists
    doctor = db.query(User).filter(User.id == booking.doctor_id, User.user_type == UserType.DOCTOR).first()
    if not doctor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found")
    
    # Check if slot is available (no bookings at that time)
    existing_booking = db.query(Booking).filter(
        Booking.doctor_id == booking.doctor_id,
        Booking.booking_time == booking.booking_time
    ).first()
    
    if existing_booking:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Slot already booked"
        )
    
    # Create booking
    db_booking = Booking(
        doctor_id=booking.doctor_id,
        patient_id=patient_id,
        booking_time=booking.booking_time,
        concern=booking.concern,
        status="scheduled"
    )
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking

def update_booking_status(db: Session, booking_id: int, booking_update: BookingUpdate):
    db_booking = get_booking(db, booking_id)
    db_booking.status = booking_update.status
    db.commit()
    db.refresh(db_booking)
    return db_booking

def get_doctor_bookings_by_date(db: Session, doctor_id: int, date: datetime):
    # Get start and end of day
    start_of_day = datetime(date.year, date.month, date.day, 0, 0, 0)
    end_of_day = datetime(date.year, date.month, date.day, 23, 59, 59)
    
    return db.query(Booking).filter(
        Booking.doctor_id == doctor_id,
        Booking.booking_time >= start_of_day,
        Booking.booking_time <= end_of_day
    ).all()

def get_available_slots(db: Session, doctor_id: int, date: datetime) -> List[AvailableSlot]:
    # Get all bookings for this doctor on this date
    bookings = get_doctor_bookings_by_date(db, doctor_id, date)
    booked_times = [booking.booking_time for booking in bookings]
    
    # Generate hourly slots (8AM to 8PM)
    slots = []
    start_time = datetime(date.year, date.month, date.day, 8, 0, 0)  # 8 AM
    end_time = datetime(date.year, date.month, date.day, 20, 0, 0)   # 8 PM
    
    current_time = start_time
    while current_time <= end_time:
        is_available = current_time not in booked_times
        
        slots.append(AvailableSlot(
            slot_time=current_time,
            is_available=is_available
        ))
        
        current_time += timedelta(hours=1)
    
    return slots 