from django.db import models
from accounts.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid

class ApplicationRecord(models.Model):
    """
    Core application record for a prospective nursing student.
    Tracks state through the multi-step application process.
    """
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('profile_started', 'Profile In Progress'),
        ('profile_complete', 'Profile Complete'),
        ('education_started', 'Education Info In Progress'),
        ('education_complete', 'Education Complete'),
        ('documents_started', 'Documents In Progress'),
        ('documents_complete', 'Documents Complete'),
        ('submitted', 'Application Submitted'),
        ('payment_pending', 'Awaiting Payment'),
        ('payment_confirmed', 'Payment Confirmed'),
        ('under_review', 'Under Review'),
        ('interview_scheduled', 'Interview Scheduled'),
        ('interview_completed', 'Interview Completed'),
        ('admitted', 'Admitted'),
        ('waitlisted', 'Waitlisted'),
        ('rejected', 'Not Admitted'),
        ('deferred', 'Application Deferred'),
    ]

    # Applicant relationship
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admission_application')
    
    # Application tracking
    application_number = models.CharField(max_length=20, unique=True, blank=True)
    academic_year = models.CharField(max_length=9, default='2025/2026')
    
    # Status tracking
    current_step = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default='not_started')
    
    # Program selection
    PROGRAM_CHOICES = [
        ('pht', 'Public Health Technology'),
        ('himt', 'Health Information Management Technology'),
        ('chew', 'Community Health Extension Workers'),
        ('pt', 'Pharmacy Technician'),
        ('mlt', 'Medical Laboratory Technician'),
    ]
    
    first_choice_program = models.CharField(max_length=4, choices=PROGRAM_CHOICES, blank=True)
    second_choice_program = models.CharField(max_length=4, choices=PROGRAM_CHOICES, blank=True)
    
    # Payment tracking
    application_fee = models.DecimalField(max_digits=10, decimal_places=2, default=5000.00)
    is_fee_paid = models.BooleanField(default=False)
    payment_reference = models.CharField(max_length=50, blank=True)
    payment_date = models.DateTimeField(null=True, blank=True)
    
    # Admission tracking
    admission_decision = models.CharField(max_length=20, blank=True, choices=[
        ('admitted', 'Admitted'),
        ('rejected', 'Rejected'),
        ('waitlisted', 'Waitlisted'),
    ])
    admission_date = models.DateTimeField(null=True, blank=True)
    admission_notes = models.TextField(blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    submitted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['application_number']),
            models.Index(fields=['academic_year']),
        ]

    def save(self, *args, **kwargs):
        if not self.application_number:
            # Generate unique application number: YCHST/ADM/YEAR/XXXX
            year = timezone.now().year
            last_record = ApplicationRecord.objects.filter(
                application_number__contains=f"YCHST/ADM/{year}/"
            ).order_by('-id').first()
            if last_record:
                last_num = int(last_record.application_number.split('/')[-1])
                new_num = last_num + 1
            else:
                new_num = 1
            self.application_number = f"YCHST/ADM/{year}/{new_num:04d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.application_number} - {self.user.get_full_name()}"
    
    @property
    def progress_percentage(self):
        """Calculate application completion percentage"""
        steps = {
            'not_started': 0,
            'profile_started': 5,
            'profile_complete': 25,
            'education_started': 35,
            'education_complete': 50,
            'documents_started': 60,
            'documents_complete': 80,
            'submitted': 95,
            'payment_pending': 95,
            'payment_confirmed': 100,
            'under_review': 100,
            'interview_scheduled': 100,
            'interview_completed': 100,
            'admitted': 100,
            'waitlisted': 100,
            'rejected': 100,
            'deferred': 50,
        }
        return steps.get(self.status, 0)

class ApplicantProfile(models.Model):
    """Comprehensive personal and biodata for nursing school applicants"""
    application = models.OneToOneField(ApplicationRecord, on_delete=models.CASCADE, related_name='profile')
    
    # Personal Information
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    alternative_phone = models.CharField(max_length=20, blank=True)
    
    # Demographics
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
    
    # Location
    residential_address = models.TextField(blank=True)
    state_of_origin = models.CharField(max_length=50, blank=True)
    lga = models.CharField(max_length=50, blank=True)
    
    # Health information (for nursing programs)
    blood_group = models.CharField(max_length=5, blank=True, choices=[
        ('O+', 'O+'),
        ('O-', 'O-'),
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
    ])
    genotype = models.CharField(max_length=5, blank=True, choices=[
        ('AA', 'AA'),
        ('AS', 'AS'),
        ('SS', 'SS'),
    ])
    
    # Health status declaration
    has_medical_conditions = models.BooleanField(default=False)
    medical_conditions_details = models.TextField(blank=True)
    has_disabilities = models.BooleanField(default=False)
    disability_details = models.TextField(blank=True)
    vaccinations_up_to_date = models.BooleanField(default=False)
    
    # Next of Kin
    nok_name = models.CharField(max_length=100, blank=True, verbose_name="Next of Kin Name")
    nok_relationship = models.CharField(max_length=50, blank=True)
    nok_phone = models.CharField(max_length=20, blank=True)
    nok_address = models.TextField(blank=True)
    
    # Employment/Background
    is_employed = models.BooleanField(default=False)
    employment_details = models.TextField(blank=True)
    has_healthcare_experience = models.BooleanField(default=False)
    healthcare_experience_details = models.TextField(blank=True)
    
    # Completed soft-delete for privacy - track completion
    profile_completed = models.BooleanField(default=False)
    profile_completed_at = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Applicant Profile"
        verbose_name_plural = "Applicant Profiles"

    def __str__(self):
        return f"Profile for {self.application.user.get_full_name()}"


class AcademicHistory(models.Model):
    """Comprehensive educational background for nursing school applicants"""
    application = models.OneToOneField(ApplicationRecord, on_delete=models.CASCADE, related_name='academic_info')
    
    # School Information
    secondary_school_name = models.CharField(max_length=200, blank=True)
    secondary_school_type = models.CharField(max_length=50, blank=True, choices=[
        ('public', 'Public School'),
        ('private', 'Private School'),
        ('tsc', 'Teachers Training College'),
        ('other', 'Other'),
    ])
    secondary_school_state = models.CharField(max_length=50, blank=True)
    year_graduated = models.PositiveIntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(1990), MaxValueValidator(2030)]
    )
    
    # O'Level Results
    olevel_sitting_count = models.PositiveIntegerField(default=1, choices=[(1, 'First Sitting'), (2, 'Second Sitting')])
    olevel_exam_type = models.CharField(max_length=20, default='WAEC', choices=[
        ('WAEC', 'WAEC'),
        ('NECO', 'NECO'),
        ('NABTEB', 'NABTEB'),
        ('GCE', 'GCE'),
    ])
    olevel_exam_year = models.PositiveIntegerField(null=True, blank=True)
    olevel_results = models.JSONField(default=dict, blank=True, help_text="Store as {Subject: Grade}")
    
    # JAMB Information
    jamb_reg_number = models.CharField(max_length=20, blank=True, unique=True)
    jamb_exam_year = models.PositiveIntegerField(null=True, blank=True)
    jamb_score = models.PositiveIntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(400)]
    )
    jamb_subject_combination = models.CharField(max_length=100, blank=True)
    
    # UTME vs Direct Entry
    ENTRY_TYPE_CHOICES = [
        ('utme', 'UTME'),
        ('direct_entry', 'Direct Entry'),
        ('transfer', 'Transfer'),
    ]
    entry_type = models.CharField(max_length=20, choices=ENTRY_TYPE_CHOICES, default='utme')
    
    # Previous tertiary education (for transfers)
    previous_institution = models.CharField(max_length=200, blank=True)
    previous_program = models.CharField(max_length=100, blank=True)
    previous_level = models.CharField(max_length=50, blank=True)
    previous_cgpa = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    
    # Transcripts and documents
    has_olevel_transcript = models.BooleanField(default=False)
    has_jamb_result_slip = models.BooleanField(default=False)
    has_birth_certificate = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Academic History"
        verbose_name_plural = "Academic Histories"

    def __str__(self):
        return f"Academic History for {self.application.user.get_full_name()}"


class AdmissionDocument(models.Model):
    """Tracks uploaded documents with validation and verification"""
    application = models.ForeignKey(ApplicationRecord, on_delete=models.CASCADE, related_name='documents')
    
    DOC_TYPE_CHOICES = [
        ('passport_photo', 'Passport Photograph (4x6)'),
        ('olevel_transcript', 'O-Level Statement of Result'),
        ('jamb_result_slip', 'JAMB Result Slip'),
        ('jamb_printout', 'JAMB Admission Printout'),
        ('birth_certificate', 'Birth Certificate / Age Declaration'),
        ('indigene_certificate', 'Local Government Indigene Certificate'),
        ('national_id', 'National ID Card'),
        ('drivers_license', 'Driver\'s License'),
        ('medical_report', 'Pre-admission Medical Report'),
        ('vaccination_card', 'Vaccination Record'),
        ('other', 'Other Supporting Document'),
    ]
    
    document_type = models.CharField(max_length=30, choices=DOC_TYPE_CHOICES)
    file = models.FileField(upload_to='admission_docs/%Y/%m/%d/')
    file_size = models.PositiveIntegerField(help_text="File size in bytes")
    
    # Validation
    is_verified = models.BooleanField(default=False)
    verification_notes = models.TextField(blank=True)
    verified_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='verified_documents')
    verified_at = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-uploaded_at']
        unique_together = ('application', 'document_type')  # One of each type per application

    def __str__(self):
        return f"{self.get_document_type_display()} for {self.application.application_number}"


class ApplicationStatusHistory(models.Model):
    """Track all status changes in the application process"""
    application = models.ForeignKey(ApplicationRecord, on_delete=models.CASCADE, related_name='history')
    
    old_status = models.CharField(max_length=25, blank=True)
    new_status = models.CharField(max_length=25)
    
    changed_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Application Status Histories"

    def __str__(self):
        return f"{self.application.application_number}: {self.old_status} → {self.new_status}"


class InterviewSchedule(models.Model):
    """Track interview scheduling for selected applicants"""
    application = models.ForeignKey(ApplicationRecord, on_delete=models.CASCADE, related_name='interviews')
    
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('no_show', 'No Show'),
        ('rescheduled', 'Rescheduled'),
    ]
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    interview_date = models.DateTimeField()
    interview_venue = models.CharField(max_length=200, blank=True)
    interviewer_name = models.CharField(max_length=100, blank=True)
    
    # Interview feedback
    score = models.PositiveIntegerField(null=True, blank=True, validators=[MaxValueValidator(100)], help_text="Interview score out of 100")
    feedback = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-interview_date']

    def __str__(self):
        return f"Interview for {self.application.application_number} on {self.interview_date.date()}"

    
    def __str__(self):
        return f"{self.get_document_type_display()} - {self.application.application_number}"
