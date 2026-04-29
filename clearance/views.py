"""
Clearance Views — Student & Staff (Registrar) facing views
==========================================================

Student views:
  - clearance_dashboard        → View clearance status + pipeline
  - pay_acceptance_fee         → Pay acceptance fee (simulated)
  - upload_clearance_document  → Upload required docs
  - delete_clearance_document  → Remove a doc before approval

Staff views (Registrar):
  - clearance_review_list      → List pending clearances
  - clearance_review_detail    → View student's docs + approve/reject
  - verify_document            → Verify individual document
  - approve_clearance          → Full clearance approval → triggers matric
  - reject_clearance           → Reject with reason

Bursary views:
  - configure_acceptance_fee   → Set acceptance fee amount
"""

import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST
from django.db import transaction
from django.db.models import Q
from django.utils import timezone
from django.conf import settings

from accounts.models import User, StudentProfile
from accounts.matric_utils import generate_matriculation_number, get_department_code
from portal.decorators import role_required, login_required_portal
from portal.utils import _audit
from notifications.models import Notification

from .models import StudentClearance, ClearanceDocument, ClearanceStatusHistory
from .forms import ClearanceDocumentUploadForm, AcceptanceFeeForm, ClearanceApprovalForm


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def _log_status_change(clearance, old_status, new_status, user=None, notes=''):
    """Log a clearance status transition to history + audit log."""
    ClearanceStatusHistory.objects.create(
        clearance=clearance,
        old_status=old_status,
        new_status=new_status,
        changed_by=user,
        notes=notes,
    )


def _get_required_doc_status(clearance):
    """Return a list of required document types with upload/verification status."""
    uploaded_docs = {
        doc.document_type: doc
        for doc in clearance.documents.all()
    }
    status_list = []
    for code, label in ClearanceDocument.REQUIRED_DOC_TYPES:
        doc = uploaded_docs.get(code)
        status_list.append({
            'code': code,
            'label': label,
            'uploaded': doc is not None,
            'doc': doc,
            'verified': doc.is_verified if doc else False,
            'rejected': bool(doc.rejection_note) if doc else False,
        })
    return status_list


# ─────────────────────────────────────────────────────────────────────────────
# STUDENT VIEWS
# ─────────────────────────────────────────────────────────────────────────────

@login_required_portal
@role_required('student')
def clearance_dashboard(request):
    """
    Main clearance page for newly admitted students.
    Shows pipeline progress, acceptance fee status, document uploads,
    and matric number once generated.
    """
    user = request.user

    # Get or show error
    try:
        clearance = user.clearance
    except StudentClearance.DoesNotExist:
        # Check if student already has matric (existing student)
        try:
            profile = user.student_profile
            if profile.matriculation_number:
                # Already fully set up — show a success page
                return render(request, 'clearance/dashboard.html', {
                    'already_complete': True,
                    'profile': profile,
                    'page_title': 'Clearance',
                })
        except StudentProfile.DoesNotExist:
            pass

        messages.info(request, 'No clearance record found. If you were recently admitted, please contact the Registrar.')
        return redirect('portal:dashboard')

    doc_status = _get_required_doc_status(clearance)

    # Check if student has matric / profile
    profile = None
    try:
        profile = user.student_profile
    except StudentProfile.DoesNotExist:
        pass

    # Pipeline steps for the UI
    pipeline_steps = [
        {
            'label': 'Admission Confirmed',
            'icon': 'check-circle',
            'done': True,
            'active': False,
        },
        {
            'label': 'Acceptance Fee Paid',
            'icon': 'credit-card',
            'done': clearance.acceptance_fee_paid,
            'active': clearance.status == 'pending_acceptance',
        },
        {
            'label': 'Documents Uploaded',
            'icon': 'file-text',
            'done': clearance.required_documents_uploaded,
            'active': clearance.status == 'pending_documents',
        },
        {
            'label': 'Clearance Approved',
            'icon': 'shield-check',
            'done': clearance.status == 'approved',
            'active': clearance.status == 'pending_approval',
        },
        {
            'label': 'Matric Number Assigned',
            'icon': 'graduation-cap',
            'done': clearance.matric_generated,
            'active': clearance.status == 'approved' and not clearance.matric_generated,
        },
        {
            'label': 'Student Activated',
            'icon': 'user-check',
            'done': clearance.is_fully_cleared,
            'active': False,
        },
    ]

    context = {
        'clearance': clearance,
        'doc_status': doc_status,
        'pipeline_steps': pipeline_steps,
        'profile': profile,
        'page_title': 'Clearance',
        'upload_form': ClearanceDocumentUploadForm(),
    }
    return render(request, 'clearance/dashboard.html', context)


@login_required_portal
@role_required('student')
@require_http_methods(['GET', 'POST'])
def pay_acceptance_fee(request):
    """Simulated acceptance fee payment page."""
    user = request.user

    try:
        clearance = user.clearance
    except StudentClearance.DoesNotExist:
        messages.error(request, 'No clearance record found.')
        return redirect('portal:dashboard')

    if clearance.acceptance_fee_paid:
        messages.info(request, 'Acceptance fee has already been paid.')
        return redirect('clearance:dashboard')

    if request.method == 'POST':
        form = AcceptanceFeeForm(request.POST)
        if form.is_valid():
            # Simulate payment
            ref = f"ACC-{uuid.uuid4().hex[:12].upper()}"
            old_status = clearance.status

            clearance.acceptance_fee_paid = True
            clearance.acceptance_payment_ref = ref
            clearance.acceptance_paid_at = timezone.now()
            clearance.status = 'pending_documents'
            clearance.save()

            _log_status_change(clearance, old_status, 'pending_documents', user,
                               f'Acceptance fee paid. Ref: {ref}')
            _audit(request, 'CLEARANCE', 'ACCEPTANCE_FEE_PAID', user.pk,
                   details=f'Acceptance fee ₦{clearance.acceptance_fee_amount} paid. Ref: {ref}')

            messages.success(request, f'Acceptance fee of ₦{clearance.acceptance_fee_amount:,.2f} paid successfully! Reference: {ref}')
            return redirect('clearance:dashboard')
    else:
        form = AcceptanceFeeForm()

    context = {
        'clearance': clearance,
        'form': form,
        'page_title': 'Pay Acceptance Fee',
    }
    return render(request, 'clearance/pay_acceptance.html', context)


@login_required_portal
@role_required('student')
@require_http_methods(['POST'])
def upload_clearance_document(request):
    """Upload a single clearance document."""
    user = request.user

    try:
        clearance = user.clearance
    except StudentClearance.DoesNotExist:
        messages.error(request, 'No clearance record found.')
        return redirect('portal:dashboard')

    if not clearance.acceptance_fee_paid:
        messages.error(request, 'You must pay the acceptance fee before uploading documents.')
        return redirect('clearance:dashboard')

    if clearance.status in ('approved',) and clearance.matric_locked:
        messages.error(request, 'Your clearance is already approved. Documents cannot be modified.')
        return redirect('clearance:dashboard')

    form = ClearanceDocumentUploadForm(request.POST, request.FILES)
    if form.is_valid():
        doc_type = form.cleaned_data['document_type']
        uploaded_file = form.cleaned_data['file']

        # Delete existing document of same type (re-upload)
        ClearanceDocument.objects.filter(
            clearance=clearance, document_type=doc_type
        ).delete()

        ClearanceDocument.objects.create(
            clearance=clearance,
            document_type=doc_type,
            file=uploaded_file,
            file_size=uploaded_file.size,
        )

        _audit(request, 'CLEARANCE', 'DOCUMENT_UPLOADED', user.pk,
               details=f'Uploaded {doc_type}')

        messages.success(request, f'{dict(ClearanceDocument.DOC_TYPE_CHOICES).get(doc_type, doc_type)} uploaded successfully!')

        # Auto-advance status if all required docs are now uploaded
        if clearance.required_documents_uploaded and clearance.status == 'pending_documents':
            old_status = clearance.status
            clearance.status = 'pending_approval'
            clearance.save(update_fields=['status', 'updated_at'])
            _log_status_change(clearance, old_status, 'pending_approval', user,
                               'All required documents uploaded')
            messages.info(request, 'All documents uploaded! Your clearance is now pending registrar approval.')

            # Notify registrar
            Notification.objects.create(
                recipient_role='registrar',
                title='New Clearance Pending Approval',
                message=f'Student {user.get_full_name()} ({user.username}) has uploaded all clearance documents and is awaiting approval.',
                notification_type='info',
            )
    else:
        for error in form.errors.values():
            messages.error(request, error[0])

    return redirect('clearance:dashboard')


@login_required_portal
@role_required('student')
@require_POST
def delete_clearance_document(request, doc_id):
    """Delete an uploaded document (only before approval)."""
    user = request.user

    try:
        clearance = user.clearance
    except StudentClearance.DoesNotExist:
        messages.error(request, 'No clearance record found.')
        return redirect('portal:dashboard')

    if clearance.status in ('approved',) and clearance.matric_locked:
        messages.error(request, 'Cannot modify documents after clearance approval.')
        return redirect('clearance:dashboard')

    doc = get_object_or_404(ClearanceDocument, pk=doc_id, clearance=clearance)
    doc_name = doc.get_document_type_display()
    doc.delete()

    # Revert status if we dropped below required docs
    if clearance.status == 'pending_approval' and not clearance.required_documents_uploaded:
        old_status = clearance.status
        clearance.status = 'pending_documents'
        clearance.save(update_fields=['status', 'updated_at'])
        _log_status_change(clearance, old_status, 'pending_documents', user,
                           f'Document removed: {doc_name}')

    _audit(request, 'CLEARANCE', 'DOCUMENT_DELETED', user.pk,
           details=f'Deleted {doc_name}')
    messages.success(request, f'{doc_name} removed.')
    return redirect('clearance:dashboard')


@login_required_portal
@role_required('student')
def submit_for_approval(request):
    """Explicitly submit clearance for registrar approval."""
    user = request.user

    try:
        clearance = user.clearance
    except StudentClearance.DoesNotExist:
        messages.error(request, 'No clearance record found.')
        return redirect('portal:dashboard')

    if not clearance.acceptance_fee_paid:
        messages.error(request, 'Acceptance fee must be paid first.')
        return redirect('clearance:dashboard')

    if not clearance.required_documents_uploaded:
        messages.error(request, 'All required documents must be uploaded first.')
        return redirect('clearance:dashboard')

    if clearance.status != 'pending_documents':
        messages.info(request, 'Your clearance has already been submitted for approval.')
        return redirect('clearance:dashboard')

    old_status = clearance.status
    clearance.status = 'pending_approval'
    clearance.save(update_fields=['status', 'updated_at'])
    _log_status_change(clearance, old_status, 'pending_approval', user,
                       'Student submitted for approval')

    # Notify registrar
    Notification.objects.create(
        recipient_role='registrar',
        title='New Clearance Pending Approval',
        message=f'Student {user.get_full_name()} has submitted clearance documents for your review.',
        notification_type='info',
    )

    _audit(request, 'CLEARANCE', 'SUBMITTED_FOR_APPROVAL', user.pk)
    messages.success(request, 'Your clearance has been submitted for registrar approval!')
    return redirect('clearance:dashboard')


# ─────────────────────────────────────────────────────────────────────────────
# STAFF VIEWS (REGISTRAR)
# ─────────────────────────────────────────────────────────────────────────────

@login_required_portal
@role_required('registrar', 'deputy_registrar', 'ict_director', 'director')
def clearance_review_list(request):
    """List students with pending clearance for review."""
    status_filter = request.GET.get('status', 'pending_approval')
    search = request.GET.get('search', '')

    clearances = StudentClearance.objects.select_related(
        'student'
    ).order_by('-updated_at')

    if status_filter:
        clearances = clearances.filter(status=status_filter)

    if search:
        clearances = clearances.filter(
            Q(student__username__icontains=search) |
            Q(student__first_name__icontains=search) |
            Q(student__last_name__icontains=search) |
            Q(student__email__icontains=search)
        )

    counts = {
        'pending_acceptance': StudentClearance.objects.filter(status='pending_acceptance').count(),
        'pending_documents': StudentClearance.objects.filter(status='pending_documents').count(),
        'pending_approval': StudentClearance.objects.filter(status='pending_approval').count(),
        'approved': StudentClearance.objects.filter(status='approved').count(),
        'rejected': StudentClearance.objects.filter(status='rejected').count(),
    }

    context = {
        'clearances': clearances,
        'current_status': status_filter,
        'search_query': search,
        'counts': counts,
        'page_title': 'Clearance Review',
    }
    return render(request, 'clearance/staff/review_list.html', context)


@login_required_portal
@role_required('registrar', 'deputy_registrar', 'ict_director', 'director')
def clearance_review_detail(request, pk):
    """View a student's clearance details + documents for review."""
    clearance = get_object_or_404(StudentClearance, pk=pk)
    doc_status = _get_required_doc_status(clearance)

    # Get the application record for context
    application = None
    try:
        application = clearance.student.admission_application
    except Exception:
        pass

    context = {
        'clearance': clearance,
        'doc_status': doc_status,
        'application': application,
        'history': clearance.history.all()[:20],
        'form': ClearanceApprovalForm(),
        'page_title': f'Clearance — {clearance.student.get_full_name()}',
    }
    return render(request, 'clearance/staff/review_detail.html', context)


@login_required_portal
@role_required('registrar', 'deputy_registrar', 'ict_director', 'director')
@require_POST
def verify_document(request, doc_id):
    """Verify (or reject) an individual clearance document."""
    doc = get_object_or_404(ClearanceDocument, pk=doc_id)
    action = request.POST.get('action', 'verify')
    rejection_note = request.POST.get('rejection_note', '')

    if action == 'verify':
        doc.is_verified = True
        doc.verified_by = request.user
        doc.verified_at = timezone.now()
        doc.rejection_note = ''
        doc.save()
        _audit(request, 'CLEARANCE', 'DOCUMENT_VERIFIED', doc.clearance.student.pk,
               details=f'Verified {doc.get_document_type_display()}')
        messages.success(request, f'{doc.get_document_type_display()} verified.')
    elif action == 'reject':
        doc.is_verified = False
        doc.rejection_note = rejection_note
        doc.save()
        _audit(request, 'CLEARANCE', 'DOCUMENT_REJECTED', doc.clearance.student.pk,
               details=f'Rejected {doc.get_document_type_display()}: {rejection_note}')
        messages.warning(request, f'{doc.get_document_type_display()} rejected.')

    return redirect('clearance:review_detail', pk=doc.clearance.pk)


@login_required_portal
@role_required('registrar', 'deputy_registrar', 'ict_director', 'director')
@require_POST
@transaction.atomic
def approve_clearance(request, pk):
    """
    Approve a student's clearance and generate their matric number.
    This is the CRITICAL step that creates the StudentProfile.
    """
    clearance = get_object_or_404(
        StudentClearance.objects.select_for_update(), pk=pk
    )

    # ── Guard: already done ──────────────────────────────────────────────
    if clearance.matric_locked:
        messages.error(request, 'Matric number has already been generated. Cannot re-approve.')
        return redirect('clearance:review_detail', pk=pk)

    # ── Guard: acceptance fee ────────────────────────────────────────────
    if not clearance.acceptance_fee_paid:
        messages.error(request, 'Cannot approve: Acceptance fee not paid.')
        return redirect('clearance:review_detail', pk=pk)

    # ── Guard: all docs verified ─────────────────────────────────────────
    if not clearance.all_documents_verified:
        messages.error(request, 'Cannot approve: Not all documents have been verified. Please verify all documents first.')
        return redirect('clearance:review_detail', pk=pk)

    # ── Get department from application ──────────────────────────────────
    student = clearance.student
    try:
        application = student.admission_application
        department = application.first_choice_program
    except Exception:
        messages.error(request, 'Cannot determine student department. Application record not found.')
        return redirect('clearance:review_detail', pk=pk)

    # ── Generate matric number ───────────────────────────────────────────
    academic_year = clearance.academic_year or settings.CURRENT_ACADEMIC_YEAR
    try:
        matric = generate_matriculation_number(
            department=department,
            academic_year=academic_year,
        )
        dept_code = get_department_code(department)
    except ValueError as e:
        messages.error(request, f'Matric generation error: {str(e)}')
        return redirect('clearance:review_detail', pk=pk)

    # ── Create StudentProfile ────────────────────────────────────────────
    dept_map = dict(StudentProfile.DEPT_CHOICES)
    full_dept_name = dept_map.get(dept_code, department)

    # Get applicant profile info if available
    state_of_origin = ''
    lga = ''
    try:
        app_profile = application.profile
        state_of_origin = app_profile.state_of_origin or ''
        lga = app_profile.lga or ''
    except Exception:
        pass

    profile, created = StudentProfile.objects.get_or_create(
        user=student,
        defaults={
            'matriculation_number': matric,
            'department_code': dept_code,
            'department': full_dept_name,
            'level': '100',
            'academic_year': academic_year,
            'admission_year': timezone.now().year,
            'state_of_origin': state_of_origin,
            'local_government': lga,
        }
    )

    if not created and not profile.matriculation_number:
        # Profile exists but no matric — assign it
        profile.matriculation_number = matric
        profile.department_code = dept_code
        profile.department = full_dept_name
        profile.save()

    # ── Update clearance record ──────────────────────────────────────────
    old_status = clearance.status
    clearance.status = 'approved'
    clearance.approved_by = request.user
    clearance.approved_at = timezone.now()
    clearance.matric_generated = True
    clearance.matric_generated_at = timezone.now()
    clearance.matric_locked = True  # Lock — no re-generation
    clearance.save()

    _log_status_change(clearance, old_status, 'approved', request.user,
                       f'Clearance approved. Matric: {matric}')

    # ── Audit & Notify ───────────────────────────────────────────────────
    _audit(request, 'CLEARANCE', 'APPROVED', student.pk,
           details=f'Clearance approved by {request.user.username}. Matric: {matric}')

    _audit(request, 'MATRIC_GENERATED', 'STUDENT', student.pk,
           new_value={'matric_number': matric, 'department': dept_code},
           details=f'Matric number generated: {matric}')

    Notification.objects.create(
        recipient=student,
        title='🎓 Clearance Approved — Matric Number Assigned!',
        message=f'Congratulations! Your clearance has been approved. Your matriculation number is: {matric}. You can now proceed to pay your school fees.',
        notification_type='success',
    )

    messages.success(request, f'✅ Clearance approved! Matric: {matric} assigned to {student.get_full_name()}')
    return redirect('clearance:review_list')


@login_required_portal
@role_required('registrar', 'deputy_registrar', 'ict_director', 'director')
@require_POST
def reject_clearance(request, pk):
    """Reject a student's clearance with a reason."""
    clearance = get_object_or_404(StudentClearance, pk=pk)
    reason = request.POST.get('reason', '').strip()

    if not reason:
        messages.error(request, 'Please provide a rejection reason.')
        return redirect('clearance:review_detail', pk=pk)

    old_status = clearance.status
    clearance.status = 'rejected'
    clearance.rejection_reason = reason
    clearance.save()

    _log_status_change(clearance, old_status, 'rejected', request.user, f'Rejected: {reason}')

    _audit(request, 'CLEARANCE', 'REJECTED', clearance.student.pk,
           details=f'Clearance rejected: {reason}')

    Notification.objects.create(
        recipient=clearance.student,
        title='Clearance Rejected',
        message=f'Your clearance has been rejected. Reason: {reason}. Please address the issues and re-submit.',
        notification_type='warning',
    )

    messages.warning(request, f'Clearance for {clearance.student.get_full_name()} has been rejected.')
    return redirect('clearance:review_list')


# ─────────────────────────────────────────────────────────────────────────────
# BURSARY VIEW — Acceptance Fee Configuration
# ─────────────────────────────────────────────────────────────────────────────

@login_required_portal
@role_required('bursary', 'ict_director')
def configure_acceptance_fee(request):
    """Allow bursary to update the default acceptance fee amount."""
    current_amount = 25000.00

    # Get the most recently created clearance to show current amount
    latest = StudentClearance.objects.order_by('-created_at').first()
    if latest:
        current_amount = latest.acceptance_fee_amount

    if request.method == 'POST':
        try:
            new_amount = float(request.POST.get('amount', 0))
            if new_amount <= 0:
                raise ValueError("Amount must be positive")

            # Update all pending clearances
            updated = StudentClearance.objects.filter(
                acceptance_fee_paid=False,
                status='pending_acceptance',
            ).update(acceptance_fee_amount=new_amount)

            _audit(request, 'CLEARANCE', 'FEE_CONFIGURED', request.user.pk,
                   details=f'Acceptance fee updated to ₦{new_amount:,.2f}. {updated} records updated.')

            messages.success(request, f'Acceptance fee updated to ₦{new_amount:,.2f}. {updated} pending record(s) updated.')
            return redirect('clearance:configure_fee')
        except (ValueError, TypeError) as e:
            messages.error(request, f'Invalid amount: {str(e)}')

    context = {
        'current_amount': current_amount,
        'pending_count': StudentClearance.objects.filter(
            acceptance_fee_paid=False, status='pending_acceptance'
        ).count(),
        'page_title': 'Configure Acceptance Fee',
    }
    return render(request, 'clearance/staff/configure_fee.html', context)
