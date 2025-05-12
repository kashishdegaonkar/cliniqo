🏥 Clinqo – Hospital Appointment Booking System API

Clinqo is a hospital appointment booking API built with FastAPI, enabling seamless interactions between patients and doctors through secure authentication and efficient scheduling.

✨ Features
	•	🔐 JWT-based Authentication (Doctors & Patients)
	•	👨‍⚕️ Doctor Profile Management
	•	👩‍💼 Patient Profile Management
	•	📅 Appointment Booking & Tracking
	•	⏰ Real-time Slot Availability

⚙️ Tech Stack
	•	Framework: FastAPI
	•	Database: SQLite
	•	Auth: JWT
	•	Validation: Pydantic
	•	ORM: SQLAlchemy

🚀 Getting Started

git clone https://github.com/yourusername/clinqo.git
cd clinqo

python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt
python main.py

API running at: http://localhost:8000

📘 API Docs
	•	Swagger UI: http://localhost:8000/docs
	•	ReDoc: http://localhost:8000/redoc

📌 Endpoints

🔐 Auth
	•	POST /auth/login – User login

🩺 Doctors
	•	POST /doctors/signup
	•	GET /doctors/
	•	GET /doctors/me
	•	GET /doctors/{doctor_id}
	•	GET /doctors/me/bookings
	•	GET /doctors/me/bookings/date

👤 Patients
	•	POST /patients/signup
	•	GET /patients/me
	•	GET /patients/me/bookings
	•	GET /patients/me/bookings/upcoming
	•	GET /patients/me/bookings/past

📅 Bookings
	•	POST /bookings/
	•	GET /bookings/{booking_id}
	•	PUT /bookings/{booking_id}/status
	•	GET /bookings/doctor/{doctor_id}/available

🧱 Project Structure

clinqo/
├── app/
│   ├── core/         # DB & Security
│   ├── models/       # SQLAlchemy Models
│   ├── schemas/      # Pydantic Schemas
│   ├── routers/      # API Routes
│   ├── services/     # Business Logic
│   └── main.py       # FastAPI App Init
├── main.py           # Entry Point
└── README.md

📄 License

Licensed under the MIT License.
