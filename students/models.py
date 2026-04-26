from django.db import models
from accounts.models import User


class CourseRegistration(models.Model):
    """Course registration model"""
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='course_registrations')
    course_code = models.CharField(max_length=10)
    course_title = models.CharField(max_length=200)
    credit_units = models.PositiveIntegerField()
    semester = models.CharField(max_length=20, choices=[
        ('first', 'First Semester'),
        ('second', 'Second Semester'),
    ])
    academic_year = models.CharField(max_length=9, help_text="e.g., 2023/2024")
    
    STATUS_CHOICES = [
        ('pending_exams', 'Pending Exams Office Approval'),
        ('pending_hod', 'Pending HOD Approval'),
        ('pending_registrar', 'Pending Registrar Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('dropped', 'Dropped'),
    ]
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending_exams'
    )
    
    # Approval tracking
    exams_approved_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, 
        related_name='exams_reg_approvals'
    )
    exams_approved_at = models.DateTimeField(null=True, blank=True)
    
    hod_approved_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, 
        related_name='hod_reg_approvals'
    )
    hod_approved_at = models.DateTimeField(null=True, blank=True)
    
    registrar_approved_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, 
        related_name='registrar_reg_approvals'
    )
    registrar_approved_at = models.DateTimeField(null=True, blank=True)
    
    rejection_reason = models.TextField(blank=True)
    
    # Timestamps
    registered_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['student', 'course_code', 'academic_year', 'semester']
        ordering = ['-registered_at']
    
    def __str__(self):
        return f"{self.student.username} - {self.course_code} ({self.academic_year})"


class ProgramChange(models.Model):
    """Program change request model"""
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='program_changes')
    
    current_program = models.CharField(max_length=100)
    requested_program = models.CharField(max_length=100)
    reason = models.TextField()
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Approval details
    approved_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='approved_program_changes'
    )
    approved_at = models.DateTimeField(null=True, blank=True)
    approval_notes = models.TextField(blank=True)
    
    # Timestamps
    requested_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-requested_at']
    
    def __str__(self):
        return f"{self.student.username} - Program Change: {self.current_program} → {self.requested_program}"


class IndexingRequest(models.Model):
    """Indexing request model for final year students"""
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='indexing_requests')
    
    # Academic information
    cgpa = models.DecimalField(max_digits=4, decimal_places=2)
    total_credits = models.PositiveIntegerField()
    graduation_year = models.PositiveIntegerField()
    
    # Required documents
    transcript_requested = models.BooleanField(default=True)
    certificate_requested = models.BooleanField(default=True)
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected'),
    ]
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Processing details
    processed_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='processed_indexing_requests'
    )
    processed_at = models.DateTimeField(null=True, blank=True)
    processing_notes = models.TextField(blank=True)
    
    # Timestamps
    requested_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-requested_at']
    
    def __str__(self):
        return f"{self.student.username} - Indexing Request ({self.graduation_year})"