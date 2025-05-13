from pydantic import BaseModel, EmailStr
from typing import Optional, List
from enum import Enum
from datetime import datetime

class UserType(str, Enum):
    DOCTOR = "doctor"
    PATIENT = "patient"

class Sex(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"

# Base User Models
class UserBase(BaseModel):
    email: EmailStr
    name: str

class UserCreate(UserBase):
    password: str
    
# Doctor Models
class DoctorBase(UserBase):
    specialisation: str
    hospital: str
    location: str
    phone_number: str
    experience_years: float

class DoctorCreate(DoctorBase):
    password: str

class DoctorResponse(DoctorBase):
    id: int
    
    class Config:
        from_attributes = True

# Patient Models
class PatientBase(UserBase):
    blood_group: str
    sex: Sex
    phone_number: Optional[str] = None

class PatientCreate(PatientBase):
    password: str

class PatientResponse(PatientBase):
    id: int
    
    class Config:
        from_attributes = True

# Token Models
class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    user_type: UserType

class TokenData(BaseModel):
    email: Optional[str] = None
    user_id: Optional[int] = None
    user_type: Optional[UserType] = None 