// Authentication management
class Auth {
    constructor() {
        this.user = null;
        this.init();
    }

    init() {
        // Check if user is already logged in
        const userData = localStorage.getItem('user');
        const token = localStorage.getItem('access_token');

        if (userData && token) {
            this.user = JSON.parse(userData);
            this.showDashboard();
        } else {
            this.showLogin();
        }
    }

    async login(username, password, otp = null) {
        try {
            const credentials = { username, password };
            if (otp) {
                credentials.otp = otp;
            }

            const data = await api.login(credentials);
            this.user = data.user;
            this.showDashboard();
            UI.showToast('Login successful', 'success');

            return true;
        } catch (error) {
            UI.showToast(error.message, 'error');
            return false;
        }
    }

    async logout() {
        try {
            await api.logout();
        } catch (error) {
            console.error('Logout error:', error);
        } finally {
            this.user = null;
            this.showLogin();
            UI.showToast('Logged out successfully', 'success');
        }
    }

    async register(userData) {
        try {
            await api.register(userData);
            UI.showToast('Registration successful! Please login.', 'success');
            return true;
        } catch (error) {
            UI.showToast(error.message, 'error');
            return false;
        }
    }

    showLogin() {
        document.getElementById('login-page').classList.remove('hidden');
        document.getElementById('dashboard').classList.add('hidden');
    }

    showDashboard() {
        document.getElementById('login-page').classList.add('hidden');
        document.getElementById('dashboard').classList.remove('hidden');

        // Update user info in navbar
        this.updateNavbar();

        // Initialize dashboard
        dashboard.init();
    }

    updateNavbar() {
        if (this.user) {
            document.getElementById('user-name').textContent = this.user.first_name + ' ' + this.user.last_name;
            document.getElementById('user-role').textContent = this.getRoleDisplay(this.user.role);
            document.getElementById('user-avatar').textContent = this.user.first_name.charAt(0).toUpperCase();
        }
    }

    getRoleDisplay(role) {
        const roleMap = {
            'student': 'Student',
            'staff': 'Staff',
            'ict_director': 'ICT Director',
            'director': 'Director'
        };
        return roleMap[role] || role;
    }

    isAuthenticated() {
        return this.user !== null && localStorage.getItem('access_token') !== null;
    }

    hasRole(role) {
        return this.user && this.user.role === role;
    }

    hasAnyRole(roles) {
        return this.user && roles.includes(this.user.role);
    }

    // Check if user can access a specific feature
    canAccess(feature) {
        if (!this.user) return false;

        const rolePermissions = {
            student: ['dashboard', 'fees', 'course_registration', 'results', 'profile', 'notifications'],
            staff: ['dashboard', 'course_allocation', 'results', 'salary', 'scoresheets', 'notifications'],
            ict_director: ['dashboard', 'notifications', 'otp_management'],
            director: ['dashboard', 'permissions', 'notifications', 'salary_verification']
        };

        return rolePermissions[this.user.role]?.includes(feature) || false;
    }
}

// Global auth instance
const auth = new Auth();