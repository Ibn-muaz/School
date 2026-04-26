from django.db import models
from accounts.models import User


class FeeStructure(models.Model):
    """Fee structure model"""
    
    level = models.CharField(max_length=10, help_text="Student level: 100, 200, 300, 400")
    program = models.CharField(max_length=100, help_text="Program type")
    academic_year = models.CharField(max_length=9, help_text="e.g., 2023/2024")
    
    # Fee components
    tuition_fee_per_unit = models.DecimalField(max_digits=12, decimal_places=2, null=True, default=0, help_text="Tuition fee per credit unit")
    acceptance_fee = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    registration_fee = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    examination_fee = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    library_fee = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    medical_fee = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    sports_fee = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    development_fee = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    hostel_fee = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    other_fees = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Status
    is_active = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['level', 'program', 'academic_year']
        ordering = ['-academic_year', 'level']
    
    @property
    def total_fee(self):
        """Dynamically calculate total fee from all components (legacy, assumes 0 units for tuition)."""
        return (
            0 +  # tuition_fee_per_unit * 0
            self.acceptance_fee +
            self.registration_fee +
            self.examination_fee +
            self.library_fee +
            self.medical_fee +
            self.sports_fee +
            self.development_fee +
            self.hostel_fee +
            self.other_fees
        )
    
    def get_total_fee(self, credit_units=0):
        """Calculate total fee with dynamic tuition based on credit units."""
        return (
            self.tuition_fee_per_unit * credit_units +
            self.acceptance_fee +
            self.registration_fee +
            self.examination_fee +
            self.library_fee +
            self.medical_fee +
            self.sports_fee +
            self.development_fee +
            self.hostel_fee +
            self.other_fees
        )
    
    def __str__(self):
        return f"{self.program} - Level {self.level} ({self.academic_year})"


class FeePayment(models.Model):
    """Fee payment model"""
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fee_payments')
    
    # Payment details
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    
    # Payment method
    PAYMENT_METHOD_CHOICES = [
        ('online', 'Online Payment'),
        ('bank_transfer', 'Bank Transfer'),
        ('cash', 'Cash'),
        ('check', 'Check'),
        ('other', 'Other'),
    ]
    
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='online')
    
    # Reference information
    transaction_reference = models.CharField(max_length=100, unique=True)
    bank_reference = models.CharField(max_length=100, blank=True)
    
    # Payment purpose
    purpose = models.TextField(blank=True, help_text="Description of what the payment covers")
    
    # Status
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Verification
    verified_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='verified_payments'
    )
    verified_at = models.DateTimeField(null=True, blank=True)
    
    # Receipt
    receipt_number = models.CharField(max_length=50, unique=True, null=True, blank=True)
    receipt_file = models.FileField(upload_to='receipts/', null=True, blank=True)
    
    # Timestamps
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-payment_date']
        indexes = [
            models.Index(fields=['student', 'status']),
            models.Index(fields=['transaction_reference']),
        ]
    
    def __str__(self):
        return f"Payment by {self.student.username} - ₦{self.amount} ({self.get_status_display()})"


class OtherPayment(models.Model):
    """Other payment model for non-tuition fees"""
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='other_payments')
    
    # Payment details
    PAYMENT_TYPE_CHOICES = [
        ('accommodation', 'Accommodation Fee'),
        ('feeding', 'Feeding Fee'),
        ('textbooks', 'Textbooks'),
        ('project', 'Project Fee'),
        ('certification', 'Certification'),
        ('late_registration', 'Late Registration'),
        ('other', 'Other'),
    ]
    
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField(blank=True)
    
    # Payment information
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=20, choices=[
        ('online', 'Online Payment'),
        ('bank_transfer', 'Bank Transfer'),
        ('cash', 'Cash'),
        ('check', 'Check'),
    ], default='online')
    
    transaction_reference = models.CharField(max_length=100, unique=True)
    
    # Status
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Verification
    verified_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='verified_other_payments'
    )
    verified_at = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-payment_date']
    
    def __str__(self):
        return f"{self.get_payment_type_display()} - {self.student.username} - ₦{self.amount}"