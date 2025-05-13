// API Configuration
const API_URL = 'http://localhost:8000';
const AVATAR_API_URL = 'https://avatar.iran.liara.run/public';

// Utility functions for API calls
const api = {
    // Generate avatar URL
    getAvatarUrl(identifier) {
        return `${AVATAR_API_URL}?username=${encodeURIComponent(identifier)}`;
    },

    // Generic fetch with authentication
    async fetchWithAuth(endpoint, options = {}) {
        const token = localStorage.getItem('token');
        const headers = {
            'Content-Type': 'application/json',
            ...(token && { 'Authorization': `Bearer ${token}` }),
            ...options.headers
        };

        try {
            const response = await fetch(`${API_URL}${endpoint}`, {
                ...options,
                headers
            });

            if (response.status === 401) {
                // Unauthorized, clear token and redirect to login
                this.logout();
                return null;
            }

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'API request failed');
            }

            return await response.json();
        } catch (error) {
            console.error('API request error:', error);
            throw error;
        }
    },

    // Authentication functions
    async login(username, password, userType) {
        try {
            const formData = new URLSearchParams();
            formData.append('username', username);
            formData.append('password', password);

            const response = await fetch(`${API_URL}/auth/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: formData
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Login failed');
            }

            const data = await response.json();
            
            // Check if user type matches
            if (data.user_type !== userType) {
                throw new Error(`Invalid credentials for ${userType} login`);
            }

            // Store token and user info
            localStorage.setItem('token', data.access_token);
            localStorage.setItem('userId', data.user_id);
            localStorage.setItem('userType', data.user_type);
            
            return data;
        } catch (error) {
            console.error('Login error:', error);
            throw error;
        }
    },

    logout() {
        localStorage.removeItem('token');
        localStorage.removeItem('userId');
        localStorage.removeItem('userType');
        
        // Redirect to home
        window.location.href = '/';
    },

    isAuthenticated() {
        return !!localStorage.getItem('token');
    },

    getUserType() {
        return localStorage.getItem('userType');
    },

    getUserId() {
        return localStorage.getItem('userId');
    },

    // Doctor API calls
    async getDoctors() {
        return this.fetchWithAuth('/doctors');
    },

    async getDoctor(id) {
        return this.fetchWithAuth(`/doctors/${id}`);
    },

    async getDoctorProfile() {
        return this.fetchWithAuth('/doctors/me');
    },

    async getDoctorBookings() {
        return this.fetchWithAuth('/doctors/me/bookings');
    },

    async getDoctorBookingsByDate(date) {
        return this.fetchWithAuth(`/doctors/me/bookings/date?date_str=${date}`);
    },

    // Patient API calls
    async getPatientProfile() {
        return this.fetchWithAuth('/patients/me');
    },

    async getPatientBookings() {
        return this.fetchWithAuth('/patients/me/bookings');
    },

    async getPatientUpcomingBookings() {
        return this.fetchWithAuth('/patients/me/bookings/upcoming');
    },

    async getPatientPastBookings() {
        return this.fetchWithAuth('/patients/me/bookings/past');
    },

    // Booking API calls
    async getAvailableSlots(doctorId, date) {
        return this.fetchWithAuth(`/bookings/doctor/${doctorId}/available?date_str=${date}`);
    },

    async createBooking(doctorId, bookingTime, concern = '') {
        return this.fetchWithAuth('/bookings', {
            method: 'POST',
            body: JSON.stringify({
                doctor_id: doctorId,
                booking_time: bookingTime,
                concern
            })
        });
    },

    async updateBookingStatus(bookingId, status) {
        return this.fetchWithAuth(`/bookings/${bookingId}/status`, {
            method: 'PUT',
            body: JSON.stringify({ status })
        });
    },

    // Registration functions
    async registerDoctor(doctorData) {
        return fetch(`${API_URL}/doctors/signup`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(doctorData)
        }).then(res => {
            if (!res.ok) {
                return res.json().then(err => { throw err; });
            }
            return res.json();
        });
    },

    async registerPatient(patientData) {
        return fetch(`${API_URL}/patients/signup`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(patientData)
        }).then(res => {
            if (!res.ok) {
                return res.json().then(err => { throw err; });
            }
            return res.json();
        });
    }
};

// Utility functions
const utils = {
    // Get avatar URL
    getAvatarUrl(identifier) {
        return `${AVATAR_API_URL}?username=${encodeURIComponent(identifier)}`;
    },

    // Format date to YYYY-MM-DD
    formatDate(date) {
        const d = new Date(date);
        let month = '' + (d.getMonth() + 1);
        let day = '' + d.getDate();
        const year = d.getFullYear();

        if (month.length < 2) month = '0' + month;
        if (day.length < 2) day = '0' + day;

        return [year, month, day].join('-');
    },

    // Format date and time for display
    formatDateTime(dateString) {
        const options = { 
            year: 'numeric', 
            month: 'long', 
            day: 'numeric', 
            hour: '2-digit', 
            minute: '2-digit'
        };
        return new Date(dateString).toLocaleString('en-US', options);
    },

    // Format time only
    formatTime(dateString) {
        const options = { hour: '2-digit', minute: '2-digit' };
        return new Date(dateString).toLocaleString('en-US', options);
    },

    // Show notification
    showNotification(message, type = 'success') {
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        // Show notification
        setTimeout(() => {
            notification.classList.add('show');
        }, 10);
        
        // Remove notification after 3 seconds
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        }, 3000);
    },

    // Redirect based on user type
    redirectToDashboard() {
        const userType = api.getUserType();
        if (userType === 'doctor') {
            window.location.href = '/doctor/upcoming-bookings.html';
        } else if (userType === 'patient') {
            window.location.href = '/user/home.html';
        }
    },

    // Protect route
    protectRoute(allowedUserType) {
        if (!api.isAuthenticated()) {
            window.location.href = allowedUserType === 'doctor' 
                ? '/doctor/login.html' 
                : '/user/login.html';
            return false;
        }
        
        const userType = api.getUserType();
        if (userType !== allowedUserType) {
            window.location.href = '/';
            return false;
        }
        
        return true;
    }
};

// Check if user is already logged in when accessing login pages
document.addEventListener('DOMContentLoaded', () => {
    const path = window.location.pathname;
    
    // Redirect to dashboard if already logged in
    if ((path.includes('/login.html') || path.includes('/signup.html')) && api.isAuthenticated()) {
        utils.redirectToDashboard();
    }
    
    // Set up logout buttons
    const logoutButtons = document.querySelectorAll('.logout-btn');
    logoutButtons.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            api.logout();
        });
    });
}); 