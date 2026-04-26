from django.db import models
from accounts.models import User


class OTPRecord(models.Model):
    """OTP record model for tracking OTP generation and usage"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='otp_records')
    otp_code = models.CharField(max_length=6)
    
    # OTP purpose
    PURPOSE_CHOICES = [
        ('login', 'Login'),
        ('password_reset', 'Password Reset'),
        ('verification', 'Account Verification'),
        ('transaction', 'Transaction Verification'),
    ]
    
    purpose = models.CharField(max_length=20, choices=PURPOSE_CHOICES, default='login')
    
    # Status
    STATUS_CHOICES = [
        ('generated', 'Generated'),
        ('used', 'Used'),
        ('expired', 'Expired'),
        ('failed', 'Failed'),
    ]
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='generated')
    
    # Timestamps
    generated_at = models.DateTimeField(auto_now_add=True)
    used_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField()
    
    # Additional info
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-generated_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['expires_at']),
        ]
    
    def __str__(self):
        return f"OTP for {self.user.username} - {self.otp_code} ({self.get_status_display()})"
    
    def is_expired(self):
        from django.utils import timezone
        return timezone.now() > self.expires_at
    
    def is_valid(self):
        return self.status == 'generated' and not self.is_expired()


class AuditLog(models.Model):
    """Append-only audit trail for all significant system actions."""

    ACTION_CHOICES = [
        ('LOGIN', 'Login'),
        ('LOGOUT', 'Logout'),
        ('FAILED_LOGIN', 'Failed Login'),
        ('PASSWORD_CHANGE', 'Password Change'),
        ('2FA_VERIFY', '2FA Verified'),
        ('SCORE_ENTRY', 'Score Entry'),
        ('SCORE_SUBMIT', 'Score Submit'),
        ('SCORE_APPROVE', 'Score Approve'),
        ('RESULT_RELEASE', 'Result Release'),
        ('PAYMENT_RECORD', 'Payment Recorded'),
        ('FEE_OVERRIDE', 'Fee Override'),
        ('RECEIPT_GENERATE', 'Receipt Generated'),
        ('USER_CREATE', 'User Created'),
        ('USER_UPDATE', 'User Updated'),
        ('ROLE_CHANGE', 'Role Changed'),
        ('ACCOUNT_LOCK', 'Account Locked'),
        ('ACCOUNT_UNLOCK', 'Account Unlocked'),
        ('PERMISSION_GRANT', 'Permission Granted'),
        ('OTP_ISSUE', 'OTP Issued'),
        ('OTP_USE', 'OTP Used'),
        ('COURSE_REGISTER', 'Course Registration'),
        ('CONFIG_CHANGE', 'Config Changed'),
        ('EXPORT', 'Data Export'),
        ('OTHER', 'Other'),
    ]

    STATUS_CHOICES = [
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('warning', 'Warning'),
    ]

    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='audit_logs'
    )
    action = models.CharField(max_length=30, choices=ACTION_CHOICES)
    resource_type = models.CharField(max_length=50, blank=True)
    resource_id = models.CharField(max_length=100, blank=True)
    old_value = models.JSONField(null=True, blank=True)
    new_value = models.JSONField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    session_id = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='success')
    details = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'action']),
            models.Index(fields=['created_at']),
            models.Index(fields=['action', 'status']),
        ]

    def __str__(self):
        user_str = self.user.username if self.user else 'anonymous'
        return f"[{self.action}] {user_str} @ {self.created_at}"

    # Prevent deletion — logs are append-only
    def delete(self, *args, **kwargs):
        raise PermissionError("Audit logs cannot be deleted.")


class GeneralPermission(models.Model):
    """Special one-time permissions granted by ICT Director via OTP approval."""

    PERMISSION_TYPE_CHOICES = [
        ('late_course_reg', 'Late Course Registration'),
        ('score_re_entry', 'Score Re-entry'),
        ('fee_override', 'Fee Override'),
        ('result_unlock', 'Result Unlock'),
        ('bulk_user_import', 'Bulk User Import'),
        ('role_escalation', 'Role Escalation'),
        ('other', 'Other'),
    ]

    permission_type = models.CharField(max_length=30, choices=PERMISSION_TYPE_CHOICES)
    granted_to = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='granted_permissions'
    )
    granted_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='permissions_granted'
    )
    otp_approved_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='otp_approved_permissions'
    )
    reason = models.TextField()
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['granted_to', 'permission_type', 'is_active']),
        ]

    def __str__(self):
        return f"{self.get_permission_type_display()} → {self.granted_to.username}"

    @property
    def is_currently_valid(self):
        from django.utils import timezone
        now = timezone.now()
        return self.is_active and self.valid_from <= now <= self.valid_to