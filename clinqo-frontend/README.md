# Clinqo Frontend

This is the frontend for Clinqo, a hospital appointment booking system. The frontend is built using plain HTML, CSS, and JavaScript to interact with the Clinqo API.

## Project Structure

```
clinqo-frontend/
├── css/
│   └── styles.css         # Main stylesheet
├── js/
│   └── main.js            # Main JavaScript file with API utilities
├── images/                # Images directory
├── doctor/                # Doctor dashboard pages
│   ├── login.html         # Doctor login page
│   ├── signup.html        # Doctor registration page
│   ├── profile.html       # Doctor profile page
│   └── upcoming-bookings.html  # Doctor's appointment dashboard
├── user/                  # Patient dashboard pages
│   ├── login.html         # Patient login page
│   ├── signup.html        # Patient registration page
│   ├── home.html          # Patient dashboard home
│   ├── new-booking.html   # Create new booking page
│   ├── bookings.html      # View all bookings page
│   └── profile.html       # Patient profile page
├── index.html             # Homepage/landing page
└── README.md              # Documentation
```

## Features

- **Authentication**: Login and signup for both doctors and patients
- **Doctor Dashboard**: View and manage upcoming appointments
- **Patient Dashboard**: Book appointments, view upcoming and past appointments
- **Profile Management**: View profile information for both doctors and patients
- **Appointment Scheduling**: Patients can book appointments with doctors
- **Responsive Design**: Mobile-friendly layout

## How to Use

1. Make sure the backend API is running on `localhost:8080`
2. Open the frontend in a web browser (either by serving it with a local server or opening the HTML files directly)
3. Navigate to the homepage and choose between doctor or patient login
4. Create an account or login with existing credentials
5. Use the dashboard to manage appointments

## API Integration

The frontend communicates with the Clinqo API for all data operations. The API endpoints are:

- `/auth` - Authentication endpoints
- `/doctors` - Doctor-related endpoints
- `/patients` - Patient-related endpoints
- `/bookings` - Booking-related endpoints

## Development

To make changes to the frontend:

1. Modify the HTML files for structure changes
2. Edit `styles.css` for styling changes
3. Update `main.js` for functionality changes

## Dependencies

- Font Awesome 6.4.0 for icons

## Browser Compatibility

The frontend is compatible with modern browsers:
- Chrome
- Firefox
- Safari
- Edge

## Screenshots

(Add screenshots of the application here)

## License

This project is licensed under the MIT License.
