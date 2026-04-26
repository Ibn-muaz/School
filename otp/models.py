from django.db import models
from accounts.models import User


class OTPSettings(models.Model):
    """OTP settings model"""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='otp_settings')
    
    # OTP preferences
    email_otp_enabled = models.BooleanField(default=True)
    sms_otp_enabled = models.BooleanField(default=False)
    
    # Security settings
    otp_expiry_minutes = models.PositiveIntegerField(default=10)
    max_attempts = models.PositiveIntegerField(default=3)
    lockout_duration_minutes = models.PositiveIntegerField(default=30)
    
    # Backup codes
    backup_codes = models.JSONField(default=list, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"OTP Settings for {self.user.username}"


class OTPAttempt(models.Model):
    """OTP attempt tracking model"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='otp_attempts')
    otp_code = models.CharField(max_length=6)
    
    # Attempt details
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    
    # Status
    STATUS_CHOICES = [
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('expired', 'Expired'),
    ]
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='failed')
    
    # Timestamps
    attempted_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-attempted_at']
        indexes = [
            models.Index(fields=['user', 'attempted_at']),
        ]
    
    def __str__(self):
        return f"OTP Attempt by {self.user.username} - {self.get_status_display()}"


class OTPBlacklist(models.Model):
    """OTP blacklist for compromised codes"""
    
    otp_code = models.CharField(max_length=6, unique=True)
    reason = models.TextField()
    
    # Blacklist details
    blacklisted_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='blacklisted_otps'
    )
    blacklisted_at = models.DateTimeField(auto_now_add=True)
    
    # Expiry
    expires_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-blacklisted_at']
    
    def __str__(self):
        return f"Blacklisted OTP: {self.otp_code}"