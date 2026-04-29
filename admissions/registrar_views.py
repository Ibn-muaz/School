"""
Registrar admission decision views.
====================================
When a student is admitted:
  1. ApplicationRecord.status → 'admitted'
  2. User.role → 'student'
  3. StudentClearance record created (status='pending_acceptance')
  4. NO matric generated here — that happens after clearance approval
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.db import transaction
from accounts.models import User, StudentProfile
from admissions.models import ApplicationRecord, ApplicantProfile, AcademicHistory, AdmissionDocument
from portal.decorators import role_required, login_required_portal
from portal.utils import _audit
from django.conf import settings


@login_required_portal
@role_required('registrar', 'director')
def registrar_application_list(request):
    """List all submitted applications for registrar review."""
    status_filter = request.GET.get('status', 'submitted')
    applications = ApplicationRecord.objects.filter(status=status_filter).select_related('user', 'profile').order_by('-submitted_at')

    context = {
        'applications': applications,
        'current_status': status_filter,
        'counts': {
            'submitted': ApplicationRecord.objects.filter(status='submitted').count(),
            'under_review': ApplicationRecord.objects.filter(status='under_review').count(),
            'admitted': ApplicationRecord.objects.filter(status='admitted').count(),
            'rejected': ApplicationRecord.objects.filter(status='rejected').count(),
        }
    }
    return render(request, 'admissions/registrar/list.html', context)


@login_required_portal
@role_required('registrar', 'director')
def registrar_application_detail(request, pk):
    """Detailed view of a single application for review."""
    application = get_object_or_404(ApplicationRecord, pk=pk)

    # Update status to under_review on first open if it's just submitted
    if application.status == 'submitted':
        application.status = 'under_review'
        application.save(update_fields=['status'])

    context = {
        'app': application,
        'profile': getattr(application, 'profile', None),
        'academic': getattr(application, 'academic_info', None),
        'documents': application.documents.all(),
    }
    return render(request, 'admissions/registrar/detail.html', context)


@login_required_portal
@role_required('registrar', 'director')
@transaction.atomic
def process_admission_decision(request, pk):
    """
    Process the final admit/reject decision.

    On admission:
      - User.role → 'student'
      - StudentClearance created (status='pending_acceptance')
      - NO matric generated (matric comes after clearance approval)
    """
    application = get_object_or_404(ApplicationRecord, pk=pk)
    decision = request.POST.get('decision')
    reason = request.POST.get('reason', '')

    if decision == 'admit':
        # 1. Update application record
        application.status = 'admitted'
        application.admission_decision = 'admitted'
        application.admission_date = timezone.now()
        application.save()

        # 2. Promote User to Student
        user = application.user
        user.role = 'student'
        user.save()

        # 3. Create StudentClearance record (starts the clearance pipeline)
        from clearance.models import StudentClearance, ClearanceStatusHistory
        academic_year = getattr(settings, 'CURRENT_ACADEMIC_YEAR', '2025/2026')

        clearance, created = StudentClearance.objects.get_or_create(
            student=user,
            defaults={
                'academic_year': academic_year,
                'status': 'pending_acceptance',
            }
        )

        if created:
            ClearanceStatusHistory.objects.create(
                clearance=clearance,
                old_status='',
                new_status='pending_acceptance',
                changed_by=request.user,
                notes=f'Admission approved. Clearance pipeline started.',
            )

        # 4. Notify the student
        from notifications.models import Notification
        Notification.objects.create(
            recipient=user,
            title='🎉 Admission Confirmed!',
            message=f'Congratulations! You have been admitted to YCHST. Please proceed to complete your clearance: pay the acceptance fee, upload documents, and await approval.',
            notification_type='success',
        )

        _audit(request, 'ADMISSION', 'ADMIT', application.pk,
               details=f'Admitted. Clearance pipeline created (no matric yet).')
        messages.success(request,
                         f'Applicant {user.get_full_name()} has been admitted! '
                         f'Clearance pipeline started — matric will be assigned after clearance approval.')

    elif decision == 'reject':
        application.status = 'rejected'
        application.admission_decision = 'rejected'
        application.admission_date = timezone.now()
        application.save()

        _audit(request, 'ADMISSION', 'REJECT', application.pk,
               details=f'Rejected: {reason}')
        messages.warning(request,
                         f'Application for {application.user.get_full_name()} has been rejected.')

    return redirect('admissions:registrar_list')
