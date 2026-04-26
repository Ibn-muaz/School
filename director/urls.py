from django.urls import path
from . import views

app_name = 'director'

urlpatterns = [
    path('dashboard/', views.director_dashboard, name='dashboard'),
    path('permission-requests/', views.PermissionRequestListView.as_view(), name='permission_requests'),
    path('permission-requests/<int:pk>/', views.PermissionRequestDetailView.as_view(), name='permission_request_detail'),
    path('permission-requests/<int:request_id>/approve/', views.approve_permission_request, name='approve_permission'),
    path('permission-requests/<int:request_id>/reject/', views.reject_permission_request, name='reject_permission'),
    path('salary-verifications/', views.SalaryVerificationListView.as_view(), name='salary_verifications'),
    path('salary-verifications/<int:pk>/', views.SalaryVerificationDetailView.as_view(), name='salary_verification_detail'),
]