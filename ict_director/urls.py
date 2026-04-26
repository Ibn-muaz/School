from django.urls import path
from . import views

app_name = 'ict_director'

urlpatterns = [
    path('dashboard/', views.ict_director_dashboard, name='dashboard'),
    path('otp-records/', views.OTPRecordListView.as_view(), name='otp_records'),
    path('generate-otp/', views.generate_otp, name='generate_otp'),
    path('reset-user-otp/', views.reset_user_otp, name='reset_user_otp'),
]