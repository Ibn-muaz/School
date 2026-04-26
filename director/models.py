from django.db import models
from accounts.models import User


class PermissionRequest(models.Model):
    """Permission request model for director approval"""
    
    REQUEST_TYPE_CHOICES = [
        ('program_change', 'Program Change'),
        ('course_withdrawal', 'Course Withdrawal'),
        ('leave_request', 'Leave Request'),
        ('special_permission', 'Special Permission'),
        ('other', 'Other'),
    ]
    
    request_type = models.CharField(max_length=20, choices=REQUEST_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    # Request details
    requested_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='permission_requests')
    requested_at = models.DateTimeField(auto_now_add=True)
    
    # Supporting documents
    supporting_document = models.FileField(upload_to='permission_documents/', null=True, blank=True)
    
    # Approval details
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('under_review', 'Under Review'),
    ]
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    approved_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='approved_permissions'
    )
    approved_at = models.DateTimeField(null=True, blank=True)
    approval_notes = models.TextField(blank=True)
    
    # Priority
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    
    # Timestamps
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-requested_at']
        indexes = [
            models.Index(fields=['status', 'priority']),
            models.Index(fields=['requested_by']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.requested_by.username} ({self.get_status_display()})"


class SalaryVerification(models.Model):
    """Salary verification request model"""
    
    staff = models.ForeignKey(User, on_delete=models.CASCADE, related_name='salary_verifications')
    
    # Verification details
    purpose = models.TextField(help_text="Purpose of salary verification")
    requested_at = models.DateTimeField(auto_now_add=True)
    
    # Required information
    include_basic_salary = models.BooleanField(default=True)
    include_allowances = models.BooleanField(default=True)
    include_deductions = models.BooleanField(default=False)
    
    # Verification period
    start_date = models.DateField()
    end_date = models.DateField()
    
    # Approval and processing
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected'),
    ]
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    processed_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='processed_salary_verifications'
    )
    processed_at = models.DateTimeField(null=True, blank=True)
    processing_notes = models.TextField(blank=True)
    
    # Generated document
    verification_document = models.FileField(upload_to='salary_verifications/', null=True, blank=True)
    
    # Timestamps
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-requested_at']
    
    def __str__(self):
        return f"Salary Verification - {self.staff.username} ({self.start_date} to {self.end_date})"