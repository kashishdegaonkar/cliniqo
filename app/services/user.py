from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user import User, Doctor, Patient, UserType
from app.schemas.user import DoctorCreate, PatientCreate
from app.core.security import get_password_hash

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_doctors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).filter(User.user_type == UserType.DOCTOR).offset(skip).limit(limit).all()

def get_doctor(db: Session, doctor_id: int):
    doctor = db.query(User).filter(User.id == doctor_id, User.user_type == UserType.DOCTOR).first()
    if doctor is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found")
    return doctor

def create_doctor(db: Session, doctor: DoctorCreate):
    # Check if email already exists
    db_user = get_user_by_email(db, email=doctor.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create doctor
    hashed_password = get_password_hash(doctor.password)
    db_doctor = Doctor(
        email=doctor.email,
        name=doctor.name,
        password=hashed_password,
        specialisation=doctor.specialisation,
        hospital=doctor.hospital,
        location=doctor.location,
        phone_number=doctor.phone_number,
        experience_years=doctor.experience_years
    )
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor

def create_patient(db: Session, patient: PatientCreate):
    # Check if email already exists
    db_user = get_user_by_email(db, email=patient.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create patient
    hashed_password = get_password_hash(patient.password)
    db_patient = Patient(
        email=patient.email,
        name=patient.name,
        password=hashed_password,
        blood_group=patient.blood_group,
        sex=patient.sex,
        phone_number=patient.phone_number
    )
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient 