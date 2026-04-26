from django.urls import path
from . import views

app_name = 'otp'

urlpatterns = [
    path('settings/', views.OTPSettingsView.as_view(), name='otp_settings'),
    path('verify/', views.verify_otp, name='verify_otp'),
    path('request/', views.request_otp, name='request_otp'),
    path('blacklist/', views.blacklist_otp, name='blacklist_otp'),
    path('stats/', views.otp_stats, name='otp_stats'),
]