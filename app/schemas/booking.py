from pydantic import BaseModel, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum

from app.schemas.user import DoctorResponse, PatientResponse

class BookingStatus(str, Enum):
    SCHEDULED = "scheduled"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class BookingBase(BaseModel):
    booking_time: datetime
    concern: Optional[str] = None

class BookingCreate(BookingBase):
    doctor_id: int
    
class BookingUpdate(BaseModel):
    status: BookingStatus

class BookingResponse(BookingBase):
    id: int
    doctor_id: int
    patient_id: int
    status: BookingStatus
    
    class Config:
        from_attributes = True

class BookingDetailResponse(BookingResponse):
    doctor: Optional[DoctorResponse] = None
    patient: Optional[PatientResponse] = None
    
    class Config:
        from_attributes = True

class AvailableSlot(BaseModel):
    slot_time: datetime
    is_available: bool = True 