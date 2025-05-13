from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship

from app.core.database import Base

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, ForeignKey("users.id"), index=True)
    patient_id = Column(Integer, ForeignKey("users.id"), index=True)
    booking_time = Column(DateTime, index=True)
    status = Column(String, default="scheduled")  # scheduled, completed, cancelled
    concern = Column(Text, nullable=True)
    
    # Relationships
    doctor = relationship("User", foreign_keys=[doctor_id], back_populates="bookings_as_doctor")
    patient = relationship("User", foreign_keys=[patient_id], back_populates="bookings_as_patient") 