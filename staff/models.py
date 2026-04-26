from django.db import models
from accounts.models import User


class CourseAllocation(models.Model):
    """Course allocation model for staff"""
    staff = models.ForeignKey(User, on_delete=models.CASCADE, related_name='course_allocations')
    course_code = models.CharField(max_length=10)
    course_title = models.CharField(max_length=200)
    credit_units = models.PositiveIntegerField()
    semester = models.CharField(max_length=20, choices=[
        ('first', 'First Semester'),
        ('second', 'Second Semester'),
    ])
    academic_year = models.CharField(max_length=9, help_text="e.g., 2023/2024")
    level = models.CharField(max_length=10, help_text="Student level: 100, 200, 300, 400")
    
    # Allocation details
    allocated_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ['staff', 'course_code', 'academic_year', 'semester']
        ordering = ['-allocated_at']
    
    def __str__(self):
        return f"{self.staff.username} - {self.course_code} ({self.academic_year})"


class Scoresheet(models.Model):
    """Scoresheet model for uploading and managing student scores"""
    course_allocation = models.ForeignKey(CourseAllocation, on_delete=models.CASCADE, related_name='scoresheets')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_scoresheets')
    
    # File information
    scoresheet_file = models.FileField(upload_to='scoresheets/')
    file_name = models.CharField(max_length=255)
    
    # Academic details
    semester = models.CharField(max_length=20, choices=[
        ('first', 'First Semester'),
        ('second', 'Second Semester'),
    ])
    academic_year = models.CharField(max_length=9, help_text="e.g., 2023/2024")
    
    # Status
    STATUS_CHOICES = [
        ('draft', 'Draft (Lecturer)'),
        ('pending_hod', 'Pending HOD Approval'),
        ('pending_exams', 'Pending Exams Moderation'),
        ('pending_dean', 'Pending Dean Review'),
        ('pending_registrar', 'Pending Registrar Publication'),
        ('published', 'Published'),
        ('rejected', 'Rejected/Returned'),
    ]
    
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='draft')
    
    # Approval Tracking
    hod_approved_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='hod_scoresheet_approvals'
    )
    hod_approved_at = models.DateTimeField(null=True, blank=True)
    
    exams_validated_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='exams_scoresheet_validations'
    )
    exams_validated_at = models.DateTimeField(null=True, blank=True)
    
    dean_reviewed_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_scoresheet_reviews'
    )
    dean_reviewed_at = models.DateTimeField(null=True, blank=True)
    
    registrar_published_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='registrar_scoresheet_publications'
    )
    registrar_published_at = models.DateTimeField(null=True, blank=True)
    
    rejection_reason = models.TextField(blank=True)
    
    # Approval details
    approved_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='approved_scoresheets'
    )
    approved_at = models.DateTimeField(null=True, blank=True)
    approval_notes = models.TextField(blank=True)
    
    # Timestamps
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.course_allocation.course_code} - {self.academic_year} ({self.get_status_display()})"


class SalaryRecord(models.Model):
    """Salary record model"""
    staff = models.ForeignKey(User, on_delete=models.CASCADE, related_name='salary_records')
    
    # Salary period
    month = models.CharField(max_length=20, choices=[
        ('january', 'January'), ('february', 'February'), ('march', 'March'),
        ('april', 'April'), ('may', 'May'), ('june', 'June'),
        ('july', 'July'), ('august', 'August'), ('september', 'September'),
        ('october', 'October'), ('november', 'November'), ('december', 'December'),
    ])
    year = models.PositiveIntegerField()
    
    # Salary components
    basic_salary = models.DecimalField(max_digits=12, decimal_places=2)
    housing_allowance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    transport_allowance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    utility_allowance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    other_allowances = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Deductions
    tax = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    pension = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    other_deductions = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Totals
    gross_salary = models.DecimalField(max_digits=12, decimal_places=2)
    total_deductions = models.DecimalField(max_digits=12, decimal_places=2)
    net_salary = models.DecimalField(max_digits=12, decimal_places=2)
    
    # Payslip
    payslip_file = models.FileField(upload_to='payslips/', null=True, blank=True)
    
    # Status
    is_paid = models.BooleanField(default=False)
    paid_at = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['staff', 'month', 'year']
        ordering = ['-year', '-month']
    
    def __str__(self):
        return f"{self.staff.username} - {self.get_month_display()} {self.year}"