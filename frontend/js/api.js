// API configuration and utilities
class API {
    constructor() {
        this.baseURL = 'http://localhost:8000/api';
        this.token = localStorage.getItem('access_token');
        this.refreshToken = localStorage.getItem('refresh_token');
    }

    // Set authentication tokens
    setTokens(access, refresh) {
        this.token = access;
        this.refreshToken = refresh;
        localStorage.setItem('access_token', access);
        localStorage.setItem('refresh_token', refresh);
    }

    // Clear authentication tokens
    clearTokens() {
        this.token = null;
        this.refreshToken = null;
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user');
    }

    // Get authorization headers
    getHeaders() {
        const headers = {
            'Content-Type': 'application/json',
        };
        if (this.token) {
            headers['Authorization'] = `Bearer ${this.token}`;
        }
        return headers;
    }

    // Generic API request method
    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const config = {
            headers: this.getHeaders(),
            ...options,
        };

        try {
            const response = await fetch(url, config);

            // Handle token refresh on 401
            if (response.status === 401 && this.refreshToken) {
                const refreshSuccess = await this.refreshAccessToken();
                if (refreshSuccess) {
                    // Retry the original request with new token
                    config.headers = this.getHeaders();
                    return fetch(url, config);
                }
            }

            return response;
        } catch (error) {
            console.error('API request failed:', error);
            throw error;
        }
    }

    // Refresh access token
    async refreshAccessToken() {
        try {
            const response = await fetch(`${this.baseURL}/auth/token/refresh/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    refresh: this.refreshToken,
                }),
            });

            if (response.ok) {
                const data = await response.json();
                this.setTokens(data.access, this.refreshToken);
                return true;
            }
        } catch (error) {
            console.error('Token refresh failed:', error);
        }
        return false;
    }

    // Authentication methods
    async login(credentials) {
        const response = await this.request('/auth/login/', {
            method: 'POST',
            body: JSON.stringify(credentials),
        });

        if (response.ok) {
            const data = await response.json();
            this.setTokens(data.tokens.access, data.tokens.refresh);
            localStorage.setItem('user', JSON.stringify(data.user));
            return data;
        } else {
            const error = await response.json();
            throw new Error(error.detail || 'Login failed');
        }
    }

    async logout() {
        try {
            await this.request('/auth/logout/', {
                method: 'POST',
                body: JSON.stringify({
                    refresh_token: this.refreshToken,
                }),
            });
        } catch (error) {
            console.error('Logout error:', error);
        } finally {
            this.clearTokens();
        }
    }

    async register(userData) {
        const response = await this.request('/auth/register/', {
            method: 'POST',
            body: JSON.stringify(userData),
        });

        if (response.ok) {
            return await response.json();
        } else {
            const error = await response.json();
            throw new Error(error.detail || 'Registration failed');
        }
    }

    // User methods
    async getProfile() {
        const response = await this.request('/auth/profile/');
        if (response.ok) {
            return await response.json();
        }
        throw new Error('Failed to get profile');
    }

    async updateProfile(userData) {
        const response = await this.request('/auth/profile/update/', {
            method: 'PATCH',
            body: JSON.stringify(userData),
        });

        if (response.ok) {
            return await response.json();
        }
        throw new Error('Failed to update profile');
    }

    // Student methods
    async getStudentDashboard() {
        const response = await this.request('/students/dashboard/');
        if (response.ok) {
            return await response.json();
        }
        throw new Error('Failed to get student dashboard');
    }

    async getCourseRegistrations() {
        const response = await this.request('/students/course-registration/');
        if (response.ok) {
            return await response.json();
        }
        throw new Error('Failed to get course registrations');
    }

    async registerCourse(courseData) {
        const response = await this.request('/students/course-registration/', {
            method: 'POST',
            body: JSON.stringify(courseData),
        });

        if (response.ok) {
            return await response.json();
        }
        throw new Error('Failed to register course');
    }

    // Staff methods
    async getStaffDashboard() {
        const response = await this.request('/staff/dashboard/');
        if (response.ok) {
            return await response.json();
        }
        throw new Error('Failed to get staff dashboard');
    }

    async getCourseAllocations() {
        const response = await this.request('/staff/course-allocations/');
        if (response.ok) {
            return await response.json();
        }
        throw new Error('Failed to get course allocations');
    }

    // Fees methods
    async getFeesDashboard() {
        const response = await this.request('/fees/dashboard/');
        if (response.ok) {
            return await response.json();
        }
        throw new Error('Failed to get fees dashboard');
    }

    async getFeePayments() {
        const response = await this.request('/fees/payments/');
        if (response.ok) {
            return await response.json();
        }
        throw new Error('Failed to get fee payments');
    }

    // Results methods
    async getResultsDashboard() {
        const response = await this.request('/results/dashboard/');
        if (response.ok) {
            return await response.json();
        }
        throw new Error('Failed to get results dashboard');
    }

    async getResults() {
        const response = await this.request('/results/');
        if (response.ok) {
            return await response.json();
        }
        throw new Error('Failed to get results');
    }

    // Notifications methods
    async getNotifications() {
        const response = await this.request('/notifications/');
        if (response.ok) {
            return await response.json();
        }
        throw new Error('Failed to get notifications');
    }

    async markNotificationRead(notificationId) {
        const response = await this.request(`/notifications/mark-read/${notificationId}/`, {
            method: 'POST',
        });

        if (response.ok) {
            return await response.json();
        }
        throw new Error('Failed to mark notification as read');
    }

    // OTP methods
    async requestOTP(purpose = 'verification') {
        const response = await this.request('/otp/request/', {
            method: 'POST',
            body: JSON.stringify({ purpose }),
        });

        if (response.ok) {
            return await response.json();
        }
        throw new Error('Failed to request OTP');
    }

    async verifyOTP(otpCode, purpose = 'verification') {
        const response = await this.request('/otp/verify/', {
            method: 'POST',
            body: JSON.stringify({ otp_code: otpCode, purpose }),
        });

        if (response.ok) {
            return await response.json();
        } else {
            const error = await response.json();
            throw new Error(error.error || 'OTP verification failed');
        }
    }

    // Generic GET request
    async get(endpoint, params = {}) {
        const urlParams = new URLSearchParams(params);
        const url = urlParams.toString() ? `${endpoint}?${urlParams}` : endpoint;
        const response = await this.request(url);
        if (response.ok) {
            return await response.json();
        }
        throw new Error(`Failed to get ${endpoint}`);
    }

    // Generic POST request
    async post(endpoint, data) {
        const response = await this.request(endpoint, {
            method: 'POST',
            body: JSON.stringify(data),
        });

        if (response.ok) {
            return await response.json();
        } else {
            const error = await response.json();
            throw new Error(error.detail || `Failed to post to ${endpoint}`);
        }
    }

    // Generic PUT request
    async put(endpoint, data) {
        const response = await this.request(endpoint, {
            method: 'PUT',
            body: JSON.stringify(data),
        });

        if (response.ok) {
            return await response.json();
        }
        throw new Error(`Failed to put to ${endpoint}`);
    }

    // Generic PATCH request
    async patch(endpoint, data) {
        const response = await this.request(endpoint, {
            method: 'PATCH',
            body: JSON.stringify(data),
        });

        if (response.ok) {
            return await response.json();
        }
        throw new Error(`Failed to patch ${endpoint}`);
    }

    // Generic DELETE request
    async delete(endpoint) {
        const response = await this.request(endpoint, {
            method: 'DELETE',
        });

        if (response.ok) {
            return true;
        }
        throw new Error(`Failed to delete ${endpoint}`);
    }
}

// Create global API instance
const api = new API();