// Dashboard management
class Dashboard {
    constructor() {
        this.currentView = 'dashboard';
        this.menuItems = {};
    }

    init() {
        this.setupMenu();
        this.loadDashboard();
        this.setupEventListeners();
    }

    setupMenu() {
        const sidebarMenu = document.getElementById('sidebar-menu');
        sidebarMenu.innerHTML = '';

        const userRole = auth.user.role;
        this.menuItems = this.getMenuItems(userRole);

        Object.entries(this.menuItems).forEach(([key, item]) => {
            const menuItem = document.createElement('div');
            menuItem.className = 'sidebar-item';
            menuItem.dataset.view = key;

            const icon = document.createElement('i');
            icon.setAttribute('data-lucide', item.icon);
            menuItem.appendChild(icon);

            const text = document.createElement('span');
            text.textContent = item.title;
            menuItem.appendChild(text);

            menuItem.addEventListener('click', () => this.switchView(key));

            sidebarMenu.appendChild(menuItem);
        });

        // Initialize Lucide icons
        lucide.createIcons();
    }

    getMenuItems(role) {
        const menus = {
            student: {
                dashboard: { title: 'Dashboard', icon: 'home' },
                fees: { title: 'Fees', icon: 'credit-card' },
                course_registration: { title: 'Course Registration', icon: 'book-open' },
                results: { title: 'Results', icon: 'file-text' },
                profile: { title: 'Profile', icon: 'user' },
                notifications: { title: 'Notifications', icon: 'bell' },
            },
            staff: {
                dashboard: { title: 'Dashboard', icon: 'home' },
                course_allocation: { title: 'Course Allocation', icon: 'book-open' },
                results: { title: 'Results', icon: 'file-text' },
                salary: { title: 'Salary', icon: 'dollar-sign' },
                scoresheets: { title: 'Scoresheets', icon: 'file-spreadsheet' },
                notifications: { title: 'Notifications', icon: 'bell' },
            },
            ict_director: {
                dashboard: { title: 'Dashboard', icon: 'home' },
                notifications: { title: 'Notifications', icon: 'bell' },
                otp_management: { title: 'OTP Management', icon: 'shield' },
            },
            director: {
                dashboard: { title: 'Dashboard', icon: 'home' },
                permissions: { title: 'Permissions', icon: 'check-circle' },
                notifications: { title: 'Notifications', icon: 'bell' },
                salary_verification: { title: 'Salary Verification', icon: 'dollar-sign' },
            }
        };

        return menus[role] || {};
    }

    setupEventListeners() {
        // Logout button
        document.getElementById('logout-btn').addEventListener('click', () => {
            auth.logout();
        });
    }

    switchView(view) {
        // Update active menu item
        document.querySelectorAll('.sidebar-item').forEach(item => {
            item.classList.remove('active');
        });

        const activeItem = document.querySelector(`[data-view="${view}"]`);
        if (activeItem) {
            activeItem.classList.add('active');
        }

        this.currentView = view;
        this.loadView(view);
    }

    async loadView(view) {
        const mainContent = document.getElementById('main-content');
        mainContent.innerHTML = '<div class="flex justify-center items-center h-64"><div class="spinner"></div></div>';

        try {
            switch (view) {
                case 'dashboard':
                    await this.loadDashboard();
                    break;
                case 'fees':
                    await this.loadFeesView();
                    break;
                case 'course_registration':
                    await this.loadCourseRegistrationView();
                    break;
                case 'results':
                    await this.loadResultsView();
                    break;
                case 'profile':
                    await this.loadProfileView();
                    break;
                case 'notifications':
                    await this.loadNotificationsView();
                    break;
                case 'course_allocation':
                    await this.loadCourseAllocationView();
                    break;
                case 'salary':
                    await this.loadSalaryView();
                    break;
                case 'scoresheets':
                    await this.loadScoresheetsView();
                    break;
                case 'otp_management':
                    await this.loadOTPManagementView();
                    break;
                case 'permissions':
                    await this.loadPermissionsView();
                    break;
                case 'salary_verification':
                    await this.loadSalaryVerificationView();
                    break;
                default:
                    mainContent.innerHTML = '<div class="text-center text-gray-500">View not found</div>';
            }
        } catch (error) {
            console.error('Error loading view:', error);
            mainContent.innerHTML = '<div class="text-center text-red-500">Error loading content</div>';
        }
    }

    async loadDashboard() {
        const mainContent = document.getElementById('main-content');

        try {
            let dashboardData;

            switch (auth.user.role) {
                case 'student':
                    dashboardData = await api.getStudentDashboard();
                    this.renderStudentDashboard(dashboardData);
                    break;
                case 'staff':
                    dashboardData = await api.getStaffDashboard();
                    this.renderStaffDashboard(dashboardData);
                    break;
                case 'ict_director':
                    dashboardData = await api.get('/ict-director/dashboard/');
                    this.renderICTDirectorDashboard(dashboardData);
                    break;
                case 'director':
                    dashboardData = await api.get('/director/dashboard/');
                    this.renderDirectorDashboard(dashboardData);
                    break;
                default:
                    mainContent.innerHTML = '<div class="text-center text-gray-500">Dashboard not available</div>';
            }
        } catch (error) {
            console.error('Error loading dashboard:', error);
            mainContent.innerHTML = '<div class="text-center text-red-500">Error loading dashboard</div>';
        }
    }

    renderStudentDashboard(data) {
        const mainContent = document.getElementById('main-content');

        const html = `
            <div class="mb-8">
                <h1 class="text-2xl font-bold text-gray-900 mb-2">Student Dashboard</h1>
                <p class="text-gray-600">Welcome back, ${auth.user.first_name}!</p>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                ${UI.createStatCard(data.profile.matriculation_number, 'Matriculation Number').outerHTML}
                ${UI.createStatCard(data.profile.level, 'Level').outerHTML}
                ${UI.createStatCard(data.profile.department, 'Department').outerHTML}
                ${UI.createStatCard(UI.formatCurrency(data.profile.total_fees_paid), 'Fees Paid').outerHTML}
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div class="card">
                    <div class="card-header">
                        <h3 class="card-title">Current Semester</h3>
                    </div>
                    <div class="card-content">
                        <p><strong>Semester:</strong> ${data.current_semester.semester}</p>
                        <p><strong>Year:</strong> ${data.current_semester.year}</p>
                        <p><strong>Registered Courses:</strong> ${data.current_semester.registered_courses}</p>
                        <p><strong>Total Credits:</strong> ${data.current_semester.total_credits}</p>
                    </div>
                </div>

                <div class="card">
                    <div class="card-header">
                        <h3 class="card-title">Academic Summary</h3>
                    </div>
                    <div class="card-content">
                        <p><strong>CGPA:</strong> ${data.academic_summary.cgpa}</p>
                        <p><strong>Pending Requests:</strong> ${data.pending_requests.program_changes + data.pending_requests.indexing_requests}</p>
                    </div>
                </div>
            </div>
        `;

        mainContent.innerHTML = html;
    }

    renderStaffDashboard(data) {
        const mainContent = document.getElementById('main-content');

        const html = `
            <div class="mb-8">
                <h1 class="text-2xl font-bold text-gray-900 mb-2">Staff Dashboard</h1>
                <p class="text-gray-600">Welcome back, ${auth.user.first_name}!</p>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                ${UI.createStatCard(data.profile.staff_id, 'Staff ID').outerHTML}
                ${UI.createStatCard(data.profile.current_rank, 'Rank').outerHTML}
                ${UI.createStatCard(data.profile.department, 'Department').outerHTML}
                ${UI.createStatCard(UI.formatCurrency(data.profile.basic_salary), 'Basic Salary').outerHTML}
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div class="card">
                    <div class="card-header">
                        <h3 class="card-title">Course Allocations</h3>
                    </div>
                    <div class="card-content">
                        <p><strong>Current Allocations:</strong> ${data.current_allocations.length}</p>
                        ${data.current_allocations.slice(0, 3).map(course =>
                            `<p>• ${course.course_code} - ${course.course_title}</p>`
                        ).join('')}
                    </div>
                </div>

                <div class="card">
                    <div class="card-header">
                        <h3 class="card-title">Recent Activity</h3>
                    </div>
                    <div class="card-content">
                        <p><strong>Recent Scoresheets:</strong> ${data.recent_scoresheets.length}</p>
                        ${data.latest_salary ? `<p><strong>Latest Salary:</strong> ${UI.formatCurrency(data.latest_salary.net_salary)} (${data.latest_salary.month} ${data.latest_salary.year})</p>` : ''}
                    </div>
                </div>
            </div>
        `;

        mainContent.innerHTML = html;
    }

    renderICTDirectorDashboard(data) {
        const mainContent = document.getElementById('main-content');

        const html = `
            <div class="mb-8">
                <h1 class="text-2xl font-bold text-gray-900 mb-2">ICT Director Dashboard</h1>
                <p class="text-gray-600">System administration and OTP management</p>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                ${UI.createStatCard(data.statistics.total_otps, 'Total OTPs').outerHTML}
                ${UI.createStatCard(data.statistics.active_otps, 'Active OTPs').outerHTML}
                ${UI.createStatCard(data.statistics.used_otps, 'Used OTPs').outerHTML}
                ${UI.createStatCard(data.statistics.expired_otps, 'Expired OTPs').outerHTML}
            </div>

            <div class="card">
                <div class="card-header">
                    <h3 class="card-title">Recent OTP Activity</h3>
                </div>
                <div class="card-content">
                    ${data.recent_activity.length > 0 ?
                        UI.createTable(
                            ['User', 'Purpose', 'Status', 'Generated'],
                            data.recent_activity.map(activity => ({
                                user: activity.user_full_name,
                                purpose: activity.purpose,
                                status: activity.status,
                                generated: UI.formatDateTime(activity.generated_at)
                            }))
                        ).outerHTML :
                        '<p class="text-gray-500">No recent OTP activity</p>'
                    }
                </div>
            </div>
        `;

        mainContent.innerHTML = html;
    }

    renderDirectorDashboard(data) {
        const mainContent = document.getElementById('main-content');

        const html = `
            <div class="mb-8">
                <h1 class="text-2xl font-bold text-gray-900 mb-2">Director Dashboard</h1>
                <p class="text-gray-600">Top management oversight</p>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                ${UI.createStatCard(data.statistics.permission_requests.total, 'Total Requests').outerHTML}
                ${UI.createStatCard(data.statistics.permission_requests.pending, 'Pending Requests').outerHTML}
                ${UI.createStatCard(data.statistics.salary_verifications.total, 'Salary Verifications').outerHTML}
                ${UI.createStatCard(data.statistics.salary_verifications.pending, 'Pending Verifications').outerHTML}
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div class="card">
                    <div class="card-header">
                        <h3 class="card-title">Recent Permission Requests</h3>
                    </div>
                    <div class="card-content">
                        ${data.recent_activities.permission_requests.length > 0 ?
                            data.recent_activities.permission_requests.map(req =>
                                `<div class="border-b border-gray-200 py-2">
                                    <p class="font-medium">${req.title}</p>
                                    <p class="text-sm text-gray-600">By: ${req.requested_by_name} | Status: ${req.status}</p>
                                </div>`
                            ).join('') :
                            '<p class="text-gray-500">No recent requests</p>'
                        }
                    </div>
                </div>

                <div class="card">
                    <div class="card-header">
                        <h3 class="card-title">Recent Salary Verifications</h3>
                    </div>
                    <div class="card-content">
                        ${data.recent_activities.salary_verifications.length > 0 ?
                            data.recent_activities.salary_verifications.map(verification =>
                                `<div class="border-b border-gray-200 py-2">
                                    <p class="font-medium">${verification.staff_name}</p>
                                    <p class="text-sm text-gray-600">Status: ${verification.status}</p>
                                </div>`
                            ).join('') :
                            '<p class="text-gray-500">No recent verifications</p>'
                        }
                    </div>
                </div>
            </div>
        `;

        mainContent.innerHTML = html;
    }

    // Placeholder methods for other views - to be implemented
    async loadFeesView() {
        const mainContent = document.getElementById('main-content');
        mainContent.innerHTML = '<div class="text-center text-gray-500">Fees view - Coming soon</div>';
    }

    async loadCourseRegistrationView() {
        const mainContent = document.getElementById('main-content');
        mainContent.innerHTML = '<div class="text-center text-gray-500">Course Registration view - Coming soon</div>';
    }

    async loadResultsView() {
        const mainContent = document.getElementById('main-content');
        mainContent.innerHTML = '<div class="text-center text-gray-500">Results view - Coming soon</div>';
    }

    async loadProfileView() {
        const mainContent = document.getElementById('main-content');
        mainContent.innerHTML = '<div class="text-center text-gray-500">Profile view - Coming soon</div>';
    }

    async loadNotificationsView() {
        const mainContent = document.getElementById('main-content');
        mainContent.innerHTML = '<div class="text-center text-gray-500">Notifications view - Coming soon</div>';
    }

    async loadCourseAllocationView() {
        const mainContent = document.getElementById('main-content');
        mainContent.innerHTML = '<div class="text-center text-gray-500">Course Allocation view - Coming soon</div>';
    }

    async loadSalaryView() {
        const mainContent = document.getElementById('main-content');
        mainContent.innerHTML = '<div class="text-center text-gray-500">Salary view - Coming soon</div>';
    }

    async loadScoresheetsView() {
        const mainContent = document.getElementById('main-content');
        mainContent.innerHTML = '<div class="text-center text-gray-500">Scoresheets view - Coming soon</div>';
    }

    async loadOTPManagementView() {
        const mainContent = document.getElementById('main-content');
        mainContent.innerHTML = '<div class="text-center text-gray-500">OTP Management view - Coming soon</div>';
    }

    async loadPermissionsView() {
        const mainContent = document.getElementById('main-content');
        mainContent.innerHTML = '<div class="text-center text-gray-500">Permissions view - Coming soon</div>';
    }

    async loadSalaryVerificationView() {
        const mainContent = document.getElementById('main-content');
        mainContent.innerHTML = '<div class="text-center text-gray-500">Salary Verification view - Coming soon</div>';
    }
}

// Global dashboard instance
const dashboard = new Dashboard();