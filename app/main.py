from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import engine
from app.models import user, booking
from app.routers import auth, doctors, patients, bookings

# Create database tables
user.Base.metadata.create_all(bind=engine)
booking.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Clinqo API",
    description="Hospital Appointment Booking System API",
    version="1.0.0",
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add routers
app.include_router(auth.router)
app.include_router(doctors.router)
app.include_router(patients.router)
app.include_router(bookings.router)

@app.get("/")
def read_root():
    return {
        "message": "Welcome to Clinqo API - Hospital Appointment Booking System",
        "docs": "/docs"
    } 