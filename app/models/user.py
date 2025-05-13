from sqlalchemy import Boolean, Column, String, Integer, Float, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
import enum

from app.core.database import Base

class UserType(str, enum.Enum):
    DOCTOR = "doctor"
    PATIENT = "patient"

class Sex(str, enum.Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    user_type = Column(String, index=True)
    
    # Common fields
    name = Column(String)
    phone_number = Column(String, nullable=True)
    
    # Doctor specific fields
    specialisation = Column(String, nullable=True)
    hospital = Column(String, nullable=True)
    location = Column(String, nullable=True)
    experience_years = Column(Float, nullable=True)
    
    # Patient specific fields
    blood_group = Column(String, nullable=True)
    sex = Column(Enum(Sex), nullable=True)
    
    # Relationships
    bookings_as_patient = relationship("Booking", back_populates="patient", foreign_keys="Booking.patient_id")
    bookings_as_doctor = relationship("Booking", back_populates="doctor", foreign_keys="Booking.doctor_id")
    
    __mapper_args__ = {
        "polymorphic_on": user_type
    }

class Doctor(User):
    __mapper_args__ = {
        "polymorphic_identity": UserType.DOCTOR
    }

class Patient(User):
    __mapper_args__ = {
        "polymorphic_identity": UserType.PATIENT
    } 