from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.utils import timezone


class User(AbstractUser):
    """
    Custom user model for Yar'yaya College of Health Science and Technology.
    Supports all 13 institutional roles plus student/applicant.
    Username stores the matric number (for students) or staff ID.
    """

    ROLE_CHOICES = [
        # Students & Applicants
        ('student', 'Student'),
        ('applicant', 'Applicant'),

        # Academic Staff
        ('lecturer', 'Lecturer'),
        ('practical_master', 'Practical Master'),

        # Department Leadership
        ('hod', 'Head of Department'),
        ('hod_coordinator', 'HOD Coordinator'),

        # Faculty & Academic Administration
        ('dean_students_affairs', 'Dean of Students Affairs'),
        ('deputy_dean_students_affairs', 'Deputy Dean of Students Affairs'),
        ('academic_secretary', 'Academic Secretary'),

        # Registry & Administration
        ('provost', 'Provost'),
        ('registrar', 'Registrar'),
        ('deputy_registrar', 'Deputy Registrar'),
        ('exams_officer', 'Exams & Records Officer'),
        ('admin_officer', 'Admin Officer'),

        # Finance
        ('bursary', 'Bursar'),

        # Support Services
        ('liaison_officer', 'Liaison Officer'),
        ('hostel_admin', 'Hostel Administrator'),
        ('ict_director', 'ICT Director'),

        # Institutional Leadership
        ('director', 'Director'),
    ]

    ROLE_BADGE_COLORS = {
        'student': 'blue',
        'applicant': 'cyan',
        'lecturer': 'teal',
        'practical_master': 'emerald',
        'hod': 'indigo',
        'hod_coordinator': 'violet',
        'dean_students_affairs': 'red',
        'deputy_dean_students_affairs': 'pink',
        'academic_secretary': 'amber',
        'provost': 'orange',
        'registrar': 'green',
        'deputy_registrar': 'lime',
        'exams_officer': 'purple',
        'admin_officer': 'sky',
        'bursary': 'yellow',
        'liaison_officer': 'cyan',
        'hostel_admin': 'orange',
        'ict_director': 'slate',
        'director': 'black',
    }

    # Allow matric numbers (with slashes) as username by removing default validator
    username = models.CharField(
        _('username'),
        max_length=50,
        unique=True,
        help_text=_('Required. 50 characters or fewer. Matric number for students.'),
        validators=[],  # Remove default validator to allow matric number format
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )

    role = models.CharField(
        max_length=30,
        choices=ROLE_CHOICES,
        default='student',
        help_text="User role in the system"
    )

    # ─── Security ─────────────────────────────────────────────────────────────
    # Force password change on first login (set True for all new students)
    must_change_password = models.BooleanField(
        default=False,
        help_text="Force user to change password on next login"
    )

    # Account lockout (brute-force protection)
    failed_login_attempts = models.PositiveIntegerField(default=0)
    account_locked_until = models.DateTimeField(null=True, blank=True)

    # Session / audit tracking
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)

    # ─── Contact ──────────────────────────────────────────────────────────────
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=17,
        blank=True,
        help_text="Phone number in international format"
    )

    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        blank=True,
        null=True
    )

    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)

    # Profile picture
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        null=True,
        blank=True
    )

    # OTP / 2FA
    is_otp_verified = models.BooleanField(default=False)
    otp_secret = models.CharField(max_length=32, blank=True, null=True)
    two_fa_enabled = models.BooleanField(default=False)

    # UI preference
    THEME_CHOICES = [('light', 'Light'), ('dark', 'Dark')]
    theme_preference = models.CharField(
        max_length=10, choices=THEME_CHOICES, default='light'
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"{self.get_full_name()} ({self.username}) - {self.get_role_display()}"

    def get_role_display(self):
        return dict(self.ROLE_CHOICES).get(self.role, self.role)

    def get_role_badge_color(self):
        return self.ROLE_BADGE_COLORS.get(self.role, 'gray')

    @property
    def is_locked(self):
        """Return True if account is currently locked out."""
        if self.account_locked_until and self.account_locked_until > timezone.now():
            return True
        return False

    def increment_failed_login(self):
        """Increment failed login counter and lock if threshold reached."""
        self.failed_login_attempts += 1
        if self.failed_login_attempts >= 5:
            from datetime import timedelta
            self.account_locked_until = timezone.now() + timedelta(minutes=15)
        self.save(update_fields=['failed_login_attempts', 'account_locked_until'])

    def reset_failed_login(self):
        """Reset counter on successful login."""
        self.failed_login_attempts = 0
        self.account_locked_until = None
        self.save(update_fields=['failed_login_attempts', 'account_locked_until'])


class StudentProfile(models.Model):
    """Extended profile for enrolled students. Biodata kept here."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')

    # ─── Academic Identity ─────────────────────────────────────────────────
    matriculation_number = models.CharField(
        max_length=30,
        unique=True,
        help_text="Official matric number e.g. YCHST/2025/2026/PHT/001"
    )

    DEPT_CHOICES = [
        ('PHT',  'Public Health Technology'),
        ('HIMT', 'Health Information Management Technology'),
        ('CHEW', 'Community Health Extension Workers'),
        ('PT',   'Pharmacy Technician'),
        ('MLT',  'Medical Laboratory Technician'),
    ]

    department_code = models.CharField(
        max_length=10,
        choices=DEPT_CHOICES,
        default='PHT',
        help_text="Department code (PHT, HIMT, CHEW, PT, MLT)"
    )
    department = models.CharField(max_length=150, help_text="Full department name")
    level = models.CharField(max_length=10, default='100', help_text="e.g., 100, 200")
    academic_year = models.CharField(max_length=9, default='2025/2026')
    admission_year = models.PositiveIntegerField(default=2025)

    # ─── Biodata (completed by student after first login) ─────────────────
    state_of_origin = models.CharField(max_length=60, blank=True)
    local_government = models.CharField(max_length=60, blank=True)
    nationality = models.CharField(max_length=50, default='Nigerian')
    religion = models.CharField(max_length=30, blank=True)
    next_of_kin_name = models.CharField(max_length=100, blank=True)
    next_of_kin_phone = models.CharField(max_length=17, blank=True)
    next_of_kin_relationship = models.CharField(max_length=50, blank=True)
    next_of_kin_address = models.TextField(blank=True)
    sponsor_name = models.CharField(max_length=100, blank=True)
    sponsor_phone = models.CharField(max_length=17, blank=True)
    sponsor_occupation = models.CharField(max_length=100, blank=True)

    # ─── Status ────────────────────────────────────────────────────────────
    is_active = models.BooleanField(default=True)
    profile_completed = models.BooleanField(
        default=False,
        help_text="True once student submits complete biodata"
    )

    # ─── Financial ─────────────────────────────────────────────────────────
    total_fees_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        verbose_name = 'Student Profile'
        verbose_name_plural = 'Student Profiles'
        ordering = ['department_code', 'matriculation_number']

    def __str__(self):
        return f"{self.user.get_full_name()} — {self.matriculation_number}"

    def get_grading_scale(self):
        """Return 5.0 for HIMT, 4.0 for all others."""
        return 5.0 if self.department_code == 'HIMT' else 4.0


class StaffProfile(models.Model):
    """Extended profile for staff members"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff_profile')

    staff_id = models.CharField(
        max_length=20,
        unique=True,
        help_text="Staff ID number"
    )
    department = models.CharField(max_length=150, blank=True)
    department_code = models.CharField(max_length=10, blank=True)

    RANK_CHOICES = [
        ('graduate_assistant', 'Graduate Assistant'),
        ('assistant_lecturer', 'Assistant Lecturer'),
        ('lecturer_ii', 'Lecturer II'),
        ('lecturer_i', 'Lecturer I'),
        ('senior_lecturer', 'Senior Lecturer'),
        ('associate_professor', 'Associate Professor'),
        ('professor', 'Professor'),
        ('administrative', 'Administrative Staff'),
    ]

    current_rank = models.CharField(
        max_length=30,
        choices=RANK_CHOICES,
        default='administrative',
        help_text="Current rank/position"
    )

    date_of_first_appointment = models.DateField(null=True, blank=True)
    date_of_current_appointment = models.DateField(null=True, blank=True)

    basic_salary = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    allowances = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Staff Profile'
        verbose_name_plural = 'Staff Profiles'

    def __str__(self):
        return f"{self.user.get_full_name()} — {self.staff_id}"