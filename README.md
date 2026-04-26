# Sanga Portal - Educational Management System

A comprehensive role-based web portal for higher institutions built with Django REST Framework (Backend) and HTML/CSS/JavaScript with Tailwind CSS (Frontend).

## Features

### User Roles
- **Student Portal**: Course registration, fees management, results viewing, program changes
- **Staff Portal**: Course allocation, result management, salary viewing, scoresheet upload
- **ICT Director Portal**: OTP management, system notifications
- **Director Portal**: Permission approvals, salary verification, general oversight

### Key Features
- Role-based access control
- JWT authentication
- OTP verification system
- Fee payment management
- Course registration system
- Result management
- Notification system
- File upload capabilities

## Tech Stack

### Backend
- Django 6.0.4
- Django REST Framework
- PostgreSQL
- JWT Authentication
- CORS headers

### Frontend
- HTML5
- CSS3 with Tailwind CSS
- Vanilla JavaScript (ES6+)
- Lucide Icons
- Fetch API for HTTP requests

## Setup Instructions

### Prerequisites
- Python 3.8+
- PostgreSQL
- Git
- Modern web browser

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd sanga-portal
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment variables**
   - Copy `.env.example` to `.env` and update the values
   - Set up PostgreSQL database
   - Configure email settings for OTP

5. **Database setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the server**
   ```bash
   python manage.py runserver
   ```

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Start the development server**
   ```bash
   python ../server.py
   ```

3. **Open your browser**
   - Backend API Info: http://localhost:8000
   - Frontend: http://localhost:3000
   - Admin Interface: http://localhost:8000/admin/

### API Endpoints

#### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout
- `POST /api/auth/token/refresh/` - Refresh JWT token

#### Student Endpoints
- `GET /api/students/dashboard/` - Student dashboard
- `GET/POST /api/students/course-registration/` - Course registration
- `GET/POST /api/students/program-change/` - Program change requests
- `GET/POST /api/students/indexing/` - Indexing requests

#### Staff Endpoints
- `GET /api/staff/dashboard/` - Staff dashboard
- `GET /api/staff/course-allocations/` - Course allocations
- `GET/POST /api/staff/scoresheets/` - Scoresheet management
- `GET /api/staff/salary-records/` - Salary records

#### Fees Endpoints
- `GET /api/fees/dashboard/` - Fees dashboard
- `GET/POST /api/fees/payments/` - Fee payments
- `POST /api/fees/initiate-payment/` - Initiate online payment

#### Results Endpoints
- `GET /api/results/dashboard/` - Results dashboard
- `GET /api/results/` - View results
- `GET/POST /api/results/transcripts/` - Transcript requests

#### Notifications
- `GET /api/notifications/` - User notifications
- `POST /api/notifications/send/` - Send notifications (admin)

#### OTP Management
- `GET/POST /api/otp/settings/` - OTP settings
- `POST /api/otp/verify/` - Verify OTP
- `POST /api/otp/request/` - Request OTP

## Database Schema

### Core Tables
- `accounts_user` - Custom user model with roles
- `accounts_studentprofile` - Student profile information
- `accounts_staffprofile` - Staff profile information

### Academic Tables
- `courses_course` - Course information
- `courses_courseoffering` - Course offerings by semester/year
- `students_courseregistration` - Student course registrations

### Financial Tables
- `fees_feestructure` - Fee structures by level/program
- `fees_feepayment` - Fee payment records
- `fees_otherpayment` - Other payment records

### Results Tables
- `results_result` - Student results
- `results_semesterresult` - Semester GPA calculations
- `results_transcript` - Transcript requests

### Administrative Tables
- `director_permissionrequest` - Permission requests
- `director_salaryverification` - Salary verification requests
- `notifications_notification` - System notifications
- `ict_director_otprecord` - OTP records

## Project Structure

```
sanga_portal/
├── manage.py
├── sanga_portal/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── accounts/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   └── urls.py
├── students/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   └── urls.py
├── staff/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   └── urls.py
├── ict_director/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   └── urls.py
├── director/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   └── urls.py
├── fees/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   └── urls.py
├── courses/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   └── urls.py
├── results/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   └── urls.py
├── notifications/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   └── urls.py
├── otp/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   └── urls.py
├── frontend/
│   ├── index.html
│   ├── css/
│   │   └── styles.css
│   └── js/
│       ├── api.js
│       ├── auth.js
│       ├── ui.js
│       ├── dashboard.js
│       └── main.js
├── server.py
├── requirements.txt
├── .env
└── README.md
```

## Security Features

- JWT token-based authentication
- Role-based access control
- OTP verification for sensitive operations
- Password hashing
- CORS protection
- Input validation

## Development

### Running Tests
```bash
python manage.py test
```

### API Testing
```bash
# Test basic connectivity
python test_api.py
```

### Code Formatting
```bash
# Install black and isort
pip install black isort

# Format code
black .
isort .
```

### API Documentation
- Access Django REST Framework browsable API at `/api/`
- Use tools like Postman for API testing

## Deployment

### Production Checklist
- Set `DEBUG=False`
- Use strong `SECRET_KEY`
- Configure PostgreSQL in production
- Set up email service
- Configure static/media file serving
- Set up HTTPS
- Configure CORS properly

### Environment Variables
```env
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain.com
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=your_db_host
EMAIL_HOST_USER=your-email@domain.com
EMAIL_HOST_PASSWORD=your-email-password
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License.