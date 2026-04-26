from django.urls import path
from . import views, registrar_views

app_name = 'admissions'

urlpatterns = [
    # Public/Applicant Routes
    path('', views.application_landing, name='landing'),
    path('signup/', views.applicant_signup, name='signup'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('resend-otp/', views.resend_otp, name='resend_otp'),
    
    # Authenticated Applicant Routes
    path('dashboard/', views.applicant_dashboard, name='dashboard'),
    path('profile/complete/', views.complete_profile, name='complete_profile'),
    path('education/', views.enter_educational_info, name='educational_info'),
    path('programs/', views.select_programs, name='select_programs'),
    path('documents/', views.upload_documents, name='upload_documents'),
    path('payment/', views.process_payment, name='payment'),
    path('review/', views.review_submission, name='review_submission'),
    path('confirmation/', views.submission_confirmation, name='submission_confirmation'),
    
    # Registrar/Admin Routes
    path('registrar/dashboard/', views.registrar_dashboard, name='registrar_dashboard'),
    path('registrar/applications/', views.review_applications, name='review_applications'),
    path('registrar/applications/<int:pk>/', views.review_application_detail, name='review_detail'),
    path('registrar/applications/<int:pk>/decision/', views.make_admission_decision, name='make_decision'),
]
