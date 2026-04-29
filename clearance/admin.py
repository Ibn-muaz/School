from django.contrib import admin
from .models import StudentClearance, ClearanceDocument, ClearanceStatusHistory


class ClearanceDocumentInline(admin.TabularInline):
    model = ClearanceDocument
    extra = 0
    readonly_fields = ('uploaded_at', 'verified_at', 'verified_by')
    fields = (
        'document_type', 'file', 'file_size',
        'is_verified', 'verified_by', 'verified_at', 'rejection_note',
    )


class ClearanceStatusHistoryInline(admin.TabularInline):
    model = ClearanceStatusHistory
    extra = 0
    readonly_fields = ('old_status', 'new_status', 'changed_by', 'notes', 'created_at')
    can_delete = False


@admin.register(StudentClearance)
class StudentClearanceAdmin(admin.ModelAdmin):
    list_display = (
        'student', 'academic_year', 'status',
        'acceptance_fee_paid', 'matric_generated', 'matric_locked',
        'created_at',
    )
    list_filter = ('status', 'academic_year', 'acceptance_fee_paid', 'matric_generated')
    search_fields = ('student__username', 'student__first_name', 'student__last_name')
    readonly_fields = ('created_at', 'updated_at', 'matric_generated_at', 'acceptance_paid_at', 'approved_at')
    inlines = [ClearanceDocumentInline, ClearanceStatusHistoryInline]

    fieldsets = (
        ('Student', {
            'fields': ('student', 'academic_year', 'status'),
        }),
        ('Acceptance Fee', {
            'fields': (
                'acceptance_fee_paid', 'acceptance_fee_amount',
                'acceptance_payment_ref', 'acceptance_paid_at',
            ),
        }),
        ('Approval', {
            'fields': ('approved_by', 'approved_at', 'rejection_reason'),
        }),
        ('Matric', {
            'fields': ('matric_generated', 'matric_generated_at', 'matric_locked'),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )


@admin.register(ClearanceDocument)
class ClearanceDocumentAdmin(admin.ModelAdmin):
    list_display = (
        'clearance', 'document_type', 'is_verified',
        'verified_by', 'uploaded_at',
    )
    list_filter = ('document_type', 'is_verified')
    search_fields = (
        'clearance__student__username',
        'clearance__student__first_name',
    )
