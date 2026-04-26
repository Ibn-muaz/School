from django.db import models
from accounts.models import User


class Notification(models.Model):
    """Notification model"""
    
    title = models.CharField(max_length=200)
    message = models.TextField()
    
    # Recipients
    recipient = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='notifications',
        null=True, 
        blank=True
    )
    
    # For role-based notifications
    recipient_role = models.CharField(
        max_length=20,
        choices=[
            ('all', 'All Users'),
            ('student', 'Students'),
            ('staff', 'Staff'),
            ('hod', 'HODs'),
            ('dean', 'Deans'),
            ('exams_officer', 'Exams Officers'),
            ('registrar', 'Registrar Office'),
            ('ict_director', 'ICT Director'),
            ('bursary', 'Bursary Office'),
        ],
        null=True,
        blank=True
    )
    
    # Notification type
    NOTIFICATION_TYPE_CHOICES = [
        ('info', 'Information'),
        ('warning', 'Warning'),
        ('success', 'Success'),
        ('error', 'Error'),
        ('announcement', 'Announcement'),
    ]
    
    notification_type = models.CharField(
        max_length=20, 
        choices=NOTIFICATION_TYPE_CHOICES, 
        default='info'
    )
    
    # Priority
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    
    # Status
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    
    # Sender
    sender = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='sent_notifications'
    )
    
    # Additional data (JSON)
    extra_data = models.JSONField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', 'is_read']),
            models.Index(fields=['recipient_role', 'created_at']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.recipient.username if self.recipient else self.get_recipient_role_display()}"


class NotificationTemplate(models.Model):
    """Notification template model"""
    
    name = models.CharField(max_length=100, unique=True)
    subject_template = models.CharField(max_length=200)
    message_template = models.TextField()
    
    # Template variables (JSON)
    variables = models.JSONField(
        default=dict,
        help_text="Available variables in the template"
    )
    
    # Usage
    usage = models.TextField(blank=True, help_text="Description of when to use this template")
    
    # Status
    is_active = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name