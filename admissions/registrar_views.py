from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.db import transaction
from accounts.models import User, StudentProfile
from accounts.matric_utils import generate_matriculation_number, get_department_code
from admissions.models import ApplicationRecord, ApplicantProfile, AcademicHistory, AdmissionDocument
from portal.decorators import role_required, login_required_portal
from portal.utils import _audit

@login_required_portal
@role_required('registrar')
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
@role_required('registrar')
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
@role_required('registrar')
@transaction.atomic
def process_admission_decision(request, pk):
    """Process the final admit/reject decision."""
    application = get_object_or_404(ApplicationRecord, pk=pk)
    decision = request.POST.get('decision')
    reason = request.POST.get('reason', '')

    if decision == 'admit':
        # 1. Update application record
        application.status = 'admitted'
        application.save()

        # 2. Promote User to Student
        user = application.user
        user.role = 'student'
        user.save()

        # 3. Generate matriculation number based on department
        try:
            # Get department from application
            program = application.first_choice_program
            
            # Generate matriculation number (format: YCHST/2025/2026/DEPT_CODE/###)
            matric = generate_matriculation_number(
                department=program,
                academic_year='2025/2026'  # Update this yearly
            )
            
            # Get department code for storing
            dept_code = get_department_code(program)
            
        except ValueError as e:
            messages.error(request, f"Error generating matriculation: {str(e)}")
            return redirect('admissions:registrar_detail', pk=pk)

        # 4. Create StudentProfile with generated matriculation number
        StudentProfile.objects.get_or_create(
            user=user,
            defaults={
                'matriculation_number': matric,
                'program': application.first_choice_program,
                'department': application.first_choice_program,
                'faculty': 'Health Sciences',
                'level': '100',
                'admission_year': timezone.now().year,
                'state_of_origin': application.profile.state_of_origin if hasattr(application, 'profile') else '',
                'local_government': application.profile.lga if hasattr(application, 'profile') else '',
            }
        )

        _audit(request, 'ADMISSION', 'ADMIT', application.pk, details=f"Admitted as {matric}")
        messages.success(request, f"Applicant {user.get_full_name()} has been admitted! Matric: {matric}")

    elif decision == 'reject':
        application.status = 'rejected'
        application.save()
        _audit(request, 'ADMISSION', 'REJECT', application.pk, details=f"Rejected: {reason}")
        messages.warning(request, f"Application for {application.user.get_full_name()} has been rejected.")

    return redirect('admissions:registrar_list')
