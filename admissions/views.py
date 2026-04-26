from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.db import transaction
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from accounts.models import User, StudentProfile
from accounts.matric_utils import generate_matriculation_number
from ict_director.models import OTPRecord
from portal.decorators import role_required, login_required_portal
from portal.utils import _audit

import random
import string
from datetime import timedelta

from .models import ApplicationRecord, ApplicantProfile, AcademicHistory, AdmissionDocument, ApplicationStatusHistory
from .forms import (
    ApplicantSignupForm, ApplicantProfileForm, AcademicHistoryForm, 
    ProgramSelectionForm, DocumentUploadForm, PaymentForm, ApplicationDecisionForm
)


# ==================== APPLICANT VIEWS ====================

def application_landing(request):
    """Landing page for admissions portal"""
    if request.user.is_authenticated and request.user.role == 'applicant':
        return redirect('admissions:dashboard')
    
    context = {
        'programs': [
            {'code': 'pht', 'name': 'Public Health Technology', 'duration': '3 years'},
            {'code': 'himt', 'name': 'Health Information Management Technology', 'duration': '3 years'},
            {'code': 'chew', 'name': 'Community Health Extension Workers', 'duration': '3 years'},
            {'code': 'pt', 'name': 'Pharmacy Technician', 'duration': '3 years'},
            {'code': 'mlt', 'name': 'Medical Laboratory Technician', 'duration': '3 years'},
        ],
        'application_fee': 5000,
    }
    return render(request, 'admissions/landing.html', context)


@require_http_methods(["GET", "POST"])
def applicant_signup(request):
    """Register new applicant account"""
    if request.user.is_authenticated:
        return redirect('admissions:dashboard')
    
    if request.method == 'POST':
        form = ApplicantSignupForm(request.POST)
        if form.is_valid():
            # Create user
            user = User.objects.create_user(
                username=form.cleaned_data['email'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                role='applicant',
                is_active=False
            )
            
            # Create application record
            app = ApplicationRecord.objects.create(user=user)
            
            # Notify Director of new registration
            from notifications.models import Notification
            Notification.objects.create(
                recipient_role='director',
                title='New Applicant Registered',
                message=f'New applicant {user.get_full_name()} ({user.email}) has registered.',
                notification_type='info'
            )
            
            # Generate and send OTP
            otp_code = ''.join(random.choices(string.digits, k=6))
            OTPRecord.objects.create(
                user=user,
                otp_code=otp_code,
                purpose='verification',
                expires_at=timezone.now() + timedelta(minutes=10),
                ip_address=request.META.get('REMOTE_ADDR'),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )
            
            # Send OTP email
            try:
                subject = "YCHST Nursing School - Email Verification"
                context = {
                    'user': user,
                    'otp_code': otp_code,
                    'app_number': app.application_number,
                }
                email_body = render_to_string('admissions/emails/otp_verification.html', context)
                send_mail(
                    subject,
                    '',
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    html_message=email_body,
                    fail_silently=False,
                )
                messages.success(request, "Account created! Check your email for OTP verification code.")
            except Exception as e:
                # Still allow continuation even if email fails
                messages.warning(request, f"Account created but email could not be sent. {str(e)}")
            
            _audit(request, 'ADMISSION', 'SIGNUP', user.pk, f"New applicant: {user.email}")
            return redirect('admissions:verify_otp', email=user.email)
    else:
        form = ApplicantSignupForm()
    
    return render(request, 'admissions/signup.html', {'form': form})


@require_http_methods(["GET", "POST"])
def verify_otp(request):
    """Verify email via OTP"""
    email = request.GET.get('email') or request.POST.get('email')
    
    if not email:
        messages.error(request, "Email is required.")
        return redirect('admissions:signup')
    
    try:
        user = User.objects.get(email=email, role='applicant')
    except User.DoesNotExist:
        messages.error(request, "Account not found.")
        return redirect('admissions:signup')
    
    if user.is_active:
        messages.info(request, "This account is already verified. Please log in.")
        return redirect('portal:login')
    
    if request.method == 'POST':
        otp_code = request.POST.get('otp')
        
        if not otp_code:
            messages.error(request, "Please enter the OTP code.")
            return render(request, 'admissions/verify_otp.html', {'email': email})
        
        try:
            otp_record = OTPRecord.objects.get(
                user=user,
                otp_code=otp_code,
                purpose='verification',
                status='generated'
            )
            
            if otp_record.is_expired():
                otp_record.status = 'expired'
                otp_record.save()
                messages.error(request, "OTP has expired. Please request a new one.")
                return render(request, 'admissions/verify_otp.html', {'email': email})
            
            # Mark OTP as used and activate user
            otp_record.status = 'used'
            otp_record.used_at = timezone.now()
            otp_record.save()
            
            user.is_active = True
            user.save()
            
            _audit(request, 'ADMISSION', 'OTP_VERIFIED', user.pk, f"Email verified: {email}")
            messages.success(request, "Email verified! You can now proceed with your application.")
            return redirect('portal:login')
            
        except OTPRecord.DoesNotExist:
            messages.error(request, "Invalid OTP code. Please try again.")
    
    return render(request, 'admissions/verify_otp.html', {'email': email})


def resend_otp(request):
    """Resend OTP to email"""
    if request.method == 'POST':
        email = request.POST.get('email')
        
        try:
            user = User.objects.get(email=email, role='applicant')
        except User.DoesNotExist:
            messages.error(request, "Account not found.")
            return redirect('admissions:signup')
        
        # Invalidate old OTPs
        OTPRecord.objects.filter(user=user, purpose='verification', status='generated').update(status='expired')
        
        # Generate new OTP
        otp_code = ''.join(random.choices(string.digits, k=6))
        OTPRecord.objects.create(
            user=user,
            otp_code=otp_code,
            purpose='verification',
            expires_at=timezone.now() + timedelta(minutes=10),
            ip_address=request.META.get('REMOTE_ADDR'),
        )
        
        # Send email
        try:
            subject = "YCHST Nursing School - New OTP Code"
            context = {'user': user, 'otp_code': otp_code}
            email_body = render_to_string('admissions/emails/otp_resend.html', context)
            send_mail(subject, '', settings.DEFAULT_FROM_EMAIL, [user.email], html_message=email_body)
            messages.success(request, "New OTP sent to your email.")
        except:
            messages.warning(request, "OTP generated but could not be sent. Check application.")
        
        return redirect('admissions:verify_otp', email=email)


@login_required_portal
@role_required('applicant')
def applicant_dashboard(request):
    """Applicant dashboard with application status"""
    application = get_object_or_404(ApplicationRecord, user=request.user)
    
    context = {
        'application': application,
        'progress': application.progress_percentage,
        'profile': getattr(application, 'profile', None),
        'academic': getattr(application, 'academic_info', None),
        'documents': application.documents.all(),
    }
    return render(request, 'admissions/applicant/dashboard.html', context)


@login_required_portal
@role_required('applicant')
@transaction.atomic
def complete_profile(request):
    """Complete personal biodata"""
    application = get_object_or_404(ApplicationRecord, user=request.user)
    profile, created = ApplicantProfile.objects.get_or_create(application=application)
    
    if request.method == 'POST':
        form = ApplicantProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            application.status = 'profile_complete'
            application.save()
            _audit(request, 'ADMISSION', 'PROFILE_COMPLETE', application.pk)
            messages.success(request, "Personal information saved successfully!")
            return redirect('admissions:dashboard')
    else:
        form = ApplicantProfileForm(instance=profile)
    
    return render(request, 'admissions/applicant/complete_profile.html', {'form': form, 'application': application})


@login_required_portal
@role_required('applicant')
@transaction.atomic
def enter_educational_info(request):
    """Enter educational background"""
    application = get_object_or_404(ApplicationRecord, user=request.user)
    academic, created = AcademicHistory.objects.get_or_create(application=application)
    
    if request.method == 'POST':
        form = AcademicHistoryForm(request.POST, instance=academic)
        if form.is_valid():
            form.save()
            application.status = 'education_complete'
            application.save()
            _audit(request, 'ADMISSION', 'EDUCATION_ENTERED', application.pk)
            messages.success(request, "Educational information saved successfully!")
            return redirect('admissions:dashboard')
    else:
        form = AcademicHistoryForm(instance=academic)
    
    return render(request, 'admissions/applicant/educational_info.html', {'form': form, 'application': application})


@login_required_portal
@role_required('applicant')
@transaction.atomic
def select_programs(request):
    """Select program choices"""
    application = get_object_or_404(ApplicationRecord, user=request.user)
    
    if request.method == 'POST':
        form = ProgramSelectionForm(request.POST)
        if form.is_valid():
            application.first_choice_program = form.cleaned_data['first_choice']
            application.second_choice_program = form.cleaned_data['second_choice']
            application.save()
            _audit(request, 'ADMISSION', 'PROGRAMS_SELECTED', application.pk)
            messages.success(request, "Program choices saved!")
            return redirect('admissions:dashboard')
    else:
        form = ProgramSelectionForm(initial={
            'first_choice': application.first_choice_program,
            'second_choice': application.second_choice_program,
        })
    
    return render(request, 'admissions/applicant/select_programs.html', {'form': form, 'application': application})


@login_required_portal
@role_required('applicant')
def upload_documents(request):
    """Upload supporting documents"""
    application = get_object_or_404(ApplicationRecord, user=request.user)
    
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.application = application
            doc.file_size = request.FILES['file'].size
            doc.save()
            messages.success(request, f"{doc.get_document_type_display()} uploaded successfully!")
            return redirect('admissions:upload_documents')
    else:
        form = DocumentUploadForm()
    
    context = {
        'application': application,
        'form': form,
        'uploaded_documents': application.documents.all(),
        'required_documents': [
            'passport_photo',
            'olevel_transcript',
            'jamb_result_slip',
            'birth_certificate',
        ]
    }
    return render(request, 'admissions/applicant/upload_documents.html', context)


@login_required_portal
@role_required('applicant')
def process_payment(request):
    """Process application fee payment"""
    application = get_object_or_404(ApplicationRecord, user=request.user)
    
    if application.is_fee_paid:
        messages.info(request, "Your application fee has already been paid.")
        return redirect('admissions:dashboard')
    
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            # In real implementation, integrate with payment gateway (Paystack, Flutterwave, etc.)
            # For now, simulate payment
            application.is_fee_paid = True
            application.payment_date = timezone.now()
            application.payment_reference = f"PAY{timezone.now().strftime('%Y%m%d%H%M%S')}"
            application.status = 'payment_confirmed'
            application.save()
            
            _audit(request, 'ADMISSION', 'PAYMENT_RECEIVED', application.pk, 
                  f"Payment Reference: {application.payment_reference}")
            
            messages.success(request, "Payment successful! Your application fee has been received.")
            return redirect('admissions:review_submission')
    else:
        form = PaymentForm()
    
    context = {
        'application': application,
        'form': form,
        'amount': application.application_fee,
    }
    return render(request, 'admissions/applicant/payment.html', context)


@login_required_portal
@role_required('applicant')
def review_submission(request):
    """Review and submit application"""
    application = get_object_or_404(ApplicationRecord, user=request.user)
    
    context = {
        'application': application,
        'profile': getattr(application, 'profile', None),
        'academic': getattr(application, 'academic_info', None),
        'documents': application.documents.all(),
    }
    
    if request.method == 'POST':
        # Check completion
        if not all([application.first_choice_program, application.is_fee_paid]):
            messages.error(request, "Please complete all required steps before submitting.")
            return render(request, 'admissions/applicant/review.html', context)
        
        # Submit application
        application.status = 'submitted'
        application.submitted_at = timezone.now()
        application.save()
        
        ApplicationStatusHistory.objects.create(
            application=application,
            old_status='payment_confirmed',
            new_status='submitted',
            notes='Application submitted by applicant'
        )
        
        _audit(request, 'ADMISSION', 'SUBMITTED', application.pk)
        messages.success(request, "Application submitted successfully!")
        
        return redirect('admissions:submission_confirmation')
    
    return render(request, 'admissions/applicant/review.html', context)


@login_required_portal
@role_required('applicant')
def submission_confirmation(request):
    """Confirmation after successful submission"""
    application = get_object_or_404(ApplicationRecord, user=request.user)
    return render(request, 'admissions/applicant/confirmation.html', {'application': application})


# ==================== REGISTRAR/ADMIN VIEWS ====================

@login_required_portal
@role_required('hod', 'dean_students_affairs', 'deputy_dean_students_affairs', 'director', 'registrar', 'provost')
def registrar_dashboard(request):
    """Registrar overview dashboard"""
    context = {
        'total_applications': ApplicationRecord.objects.count(),
        'submitted': ApplicationRecord.objects.filter(status__in=['submitted', 'under_review']).count(),
        'admitted': ApplicationRecord.objects.filter(admission_decision='admitted').count(),
        'rejected': ApplicationRecord.objects.filter(admission_decision='rejected').count(),
        'recent_submissions': ApplicationRecord.objects.filter(status='submitted').order_by('-submitted_at')[:10],
    }
    return render(request, 'admissions/registrar/list.html', context)


@login_required_portal
@role_required('registrar')
def review_applications(request):
    """List applications for review"""
    from django.db.models import Q
    
    status_filter = request.GET.get('status', 'submitted')
    search = request.GET.get('search', '')
    
    applications = ApplicationRecord.objects.filter(status=status_filter).select_related('user')
    
    if search:
        applications = applications.filter(
            Q(application_number__icontains=search) |
            Q(user__email__icontains=search) |
            Q(user__first_name__icontains=search) |
            Q(user__last_name__icontains=search)
        )
    
    from .models import ApplicationRecord
    counts = {
        'submitted': ApplicationRecord.objects.filter(status='submitted').count(),
        'under_review': ApplicationRecord.objects.filter(status='under_review').count(),
        'admitted': ApplicationRecord.objects.filter(status='admitted').count(),
        'rejected': ApplicationRecord.objects.filter(status='rejected').count(),
    }
    
    context = {
        'applications': applications,
        'current_status': status_filter,
        'search_query': search,
        'status_choices': ApplicationRecord.STATUS_CHOICES,
        'counts': counts,
    }
    return render(request, 'admissions/registrar/list.html', context)


@login_required_portal
@role_required('registrar')
def review_application_detail(request, pk):
    """Detailed review of application"""
    application = get_object_or_404(ApplicationRecord, pk=pk)
    
    # Mark as under_review
    if application.status == 'submitted':
        application.status = 'under_review'
        application.save()
        ApplicationStatusHistory.objects.create(
            application=application,
            old_status='submitted',
            new_status='under_review',
            changed_by=request.user,
            notes='Application opened for review'
        )
    
    context = {
        'application': application,
        'profile': getattr(application, 'profile', None),
        'academic': getattr(application, 'academic_info', None),
        'documents': application.documents.all(),
        'history': application.history.all(),
    }
    return render(request, 'admissions/registrar/detail.html', context)


@login_required_portal
@role_required('registrar')
@transaction.atomic
def make_admission_decision(request, pk):
    """Make admission decision"""
    application = get_object_or_404(ApplicationRecord, pk=pk)
    
    if request.method == 'POST':
        form = ApplicationDecisionForm(request.POST, instance=application)
        if form.is_valid():
            decision = form.cleaned_data['admission_decision']
            
            if decision == 'admitted':
                # Promote to student
                user = application.user
                user.role = 'student'
                user.save()
                
                # Generate matriculation number
                try:
                    matric = generate_matriculation_number(
                        department=application.first_choice_program,
                        academic_year='2025/2026'
                    )
                    
                    # Create student profile
                    StudentProfile.objects.get_or_create(
                        user=user,
                        defaults={
                            'matriculation_number': matric,
                            'department': application.first_choice_program,
                            'level': '100',
                            'admission_year': timezone.now().year,
                            'state_of_origin': application.profile.state_of_origin if hasattr(application, 'profile') else '',
                            'local_government': application.profile.lga if hasattr(application, 'profile') else '',
                        }
                    )
                except Exception as e:
                    messages.error(request, f"Error generating matriculation: {str(e)}")
                    return redirect('admissions:review_detail', pk=pk)
            
            # Save decision
            application.admission_decision = decision
            application.status = f'admitted' if decision == 'admitted' else 'rejected' if decision == 'rejected' else 'waitlisted'
            application.admission_date = timezone.now()
            form.save()
            application.save()
            
            # Record history
            ApplicationStatusHistory.objects.create(
                application=application,
                new_status=application.status,
                changed_by=request.user,
                notes=f"{decision.upper()}: {form.cleaned_data['admission_notes']}"
            )
            
            _audit(request, 'ADMISSION', f'DECISION_{decision.upper()}', application.pk)
            messages.success(request, f"Application decision recorded: {decision.upper()}")
            
            return redirect('admissions:review_applications')
    else:
        form = ApplicationDecisionForm(instance=application)
    
    return render(request, 'admissions/registrar/make_decision.html', {'form': form, 'application': application})
