// Main application entry point
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Lucide icons
    lucide.createIcons();

    // Initialize authentication
    auth.init();

    // Login form handling
    const loginForm = document.getElementById('login-form');
    const loginBtn = document.getElementById('login-btn');
    const requestOtpBtn = document.getElementById('request-otp-btn');

    loginForm.addEventListener('submit', async function(e) {
        e.preventDefault();

        const formData = new FormData(loginForm);
        const username = formData.get('username');
        const password = formData.get('password');
        const otp = formData.get('otp');

        const resetLoading = UI.showLoading('login-btn', 'Signing in...');

        try {
            const success = await auth.login(username, password, otp);
            if (success) {
                loginForm.reset();
            }
        } catch (error) {
            console.error('Login error:', error);
        } finally {
            resetLoading();
        }
    });

    // OTP request handling
    if (requestOtpBtn) {
        requestOtpBtn.addEventListener('click', async function() {
            const username = document.getElementById('username').value;

            if (!username) {
                UI.showToast('Please enter username first', 'warning');
                return;
            }

            try {
                // For demo purposes, we'll show the OTP section
                // In production, this would make an API call
                document.getElementById('otp-section').classList.remove('hidden');
                UI.showToast('OTP sent to your registered email/phone', 'success');
            } catch (error) {
                UI.showToast('Failed to request OTP', 'error');
            }
        });
    }

    // Modal close on overlay click
    document.getElementById('modal-overlay').addEventListener('click', function(e) {
        if (e.target === this) {
            UI.hideModal();
        }
    });

    // Global error handler
    window.addEventListener('unhandledrejection', function(event) {
        console.error('Unhandled promise rejection:', event.reason);
        UI.showToast('An unexpected error occurred', 'error');
    });

    // Service worker registration (for PWA features - optional)
    if ('serviceWorker' in navigator) {
        window.addEventListener('load', function() {
            // navigator.serviceWorker.register('/sw.js');
        });
    }

    console.log('Sanga Portal initialized successfully');
});