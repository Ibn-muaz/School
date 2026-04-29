"""
Student Clearance Module — Models
=================================
Tracks the clearance pipeline for newly admitted students:
  Acceptance Fee → Document Upload → Registrar Approval → Matric Generation → Activated

Clearance is the gateway between admission and becoming a fully enrolled student.
"""

from django.db import models
from django.conf import settings
from django.utils import timezone
from accounts.models import User


class StudentClearance(models.Model):
    """
    One-per-student clearance record that tracks progress through the
    post-admission pipeline.
    """
    student = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='clearance'
    )
    academic_year = models.CharField(
        max_length=9,
        default='2025/2026',
        help_text="Academic year for this clearance cycle"
    )

    # ─── Status Pipeline ──────────────────────────────────────────────────
    STATUS_CHOICES = [
        ('pending_acceptance', 'Awaiting Acceptance Fee'),
        ('pending_documents', 'Awaiting Document Upload'),
        ('pending_approval', 'Awaiting Registrar Approval'),
        ('approved', 'Clearance Approved'),
        ('rejected', 'Clearance Rejected'),
    ]
    status = models.CharField(
        max_length=25,
        choices=STATUS_CHOICES,
        default='pending_acceptance',
        help_text="Current stage in the clearance pipeline"
    )

    # ─── Acceptance Fee ───────────────────────────────────────────────────
    acceptance_fee_paid = models.BooleanField(default=False)
    acceptance_fee_amount = models.DecimalField(
        max_digits=12, decimal_places=2, default=25000.00,
        help_text="Amount charged for acceptance fee (configurable by Bursary)"
    )
    acceptance_payment_ref = models.CharField(
        max_length=100, blank=True,
        help_text="Payment reference for acceptance fee"
    )
    acceptance_paid_at = models.DateTimeField(null=True, blank=True)

    # ─── Registrar Approval ──────────────────────────────────────────────
    approved_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='clearances_approved',
        help_text="Registrar who approved this clearance"
    )
    approved_at = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(
        blank=True,
        help_text="Reason for rejection (if rejected)"
    )

    # ─── Matric Tracking ─────────────────────────────────────────────────
    matric_generated = models.BooleanField(
        default=False,
        help_text="True once matriculation number has been assigned"
    )
    matric_generated_at = models.DateTimeField(null=True, blank=True)
    matric_locked = models.BooleanField(
        default=False,
        help_text="Once True, matric cannot be regenerated"
    )

    # ─── Timestamps ──────────────────────────────────────────────────────
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Student Clearance'
        verbose_name_plural = 'Student Clearances'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['student', 'status']),
            models.Index(fields=['academic_year', 'status']),
        ]

    def __str__(self):
        return f"{self.student.get_full_name()} — {self.get_status_display()}"

    @property
    def is_fully_cleared(self):
        """True if the student has completed the full clearance pipeline."""
        return self.status == 'approved' and self.matric_generated

    @property
    def progress_percentage(self):
        """Return a numeric progress value for the pipeline UI."""
        progress_map = {
            'pending_acceptance': 10,
            'pending_documents': 30,
            'pending_approval': 60,
            'approved': 90,
        }
        base = progress_map.get(self.status, 0)
        if self.status == 'approved' and self.matric_generated:
            return 100
        return base

    @property
    def required_documents_uploaded(self):
        """Check if all mandatory document types have been uploaded."""
        required_types = {dt[0] for dt in ClearanceDocument.REQUIRED_DOC_TYPES}
        uploaded_types = set(
            self.documents.values_list('document_type', flat=True)
        )
        return required_types.issubset(uploaded_types)

    @property
    def all_documents_verified(self):
        """Check if all uploaded documents have been verified."""
        docs = self.documents.all()
        if not docs.exists():
            return False
        return not docs.filter(is_verified=False).exists()


class ClearanceDocument(models.Model):
    """
    Individual document uploaded during the clearance process.
    Each document goes through upload → verification by registrar.
    """
    clearance = models.ForeignKey(
        StudentClearance, on_delete=models.CASCADE, related_name='documents'
    )

    DOC_TYPE_CHOICES = [
        ('waec_neco', 'WAEC/NECO Result'),
        ('birth_certificate', 'Birth Certificate'),
        ('passport_photo', 'Passport Photograph'),
        ('acceptance_letter', 'Acceptance Letter'),
        ('lga_certificate', 'LGA Identification'),
        ('medical_report', 'Medical Report'),
        ('other', 'Other Supporting Document'),
    ]

    # All types except 'other' are mandatory
    REQUIRED_DOC_TYPES = [
        ('waec_neco', 'WAEC/NECO Result'),
        ('birth_certificate', 'Birth Certificate'),
        ('passport_photo', 'Passport Photograph'),
        ('acceptance_letter', 'Acceptance Letter'),
        ('lga_certificate', 'LGA Identification'),
        ('medical_report', 'Medical Report'),
    ]

    document_type = models.CharField(
        max_length=25, choices=DOC_TYPE_CHOICES,
        help_text="Type of clearance document"
    )
    file = models.FileField(
        upload_to='clearance_docs/%Y/',
        help_text="Uploaded document file"
    )
    file_size = models.PositiveIntegerField(
        help_text="File size in bytes"
    )

    # ─── Verification ────────────────────────────────────────────────────
    is_verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='verified_clearance_docs'
    )
    verified_at = models.DateTimeField(null=True, blank=True)
    rejection_note = models.TextField(
        blank=True,
        help_text="Reason for document rejection"
    )

    # ─── Timestamps ──────────────────────────────────────────────────────
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Clearance Document'
        verbose_name_plural = 'Clearance Documents'
        ordering = ['document_type']
        unique_together = ('clearance', 'document_type')

    def __str__(self):
        return f"{self.get_document_type_display()} — {self.clearance.student.get_full_name()}"


class ClearanceStatusHistory(models.Model):
    """
    Audit trail for every status change in the clearance pipeline.
    """
    clearance = models.ForeignKey(
        StudentClearance, on_delete=models.CASCADE, related_name='history'
    )
    old_status = models.CharField(max_length=25, blank=True)
    new_status = models.CharField(max_length=25)
    changed_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Clearance Status History'
        verbose_name_plural = 'Clearance Status Histories'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.clearance.student.username}: {self.old_status} → {self.new_status}"
