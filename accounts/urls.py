from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/update/', views.ProfileUpdateView.as_view(), name='profile_update'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change_password'),
    path('student-profile/', views.StudentProfileView.as_view(), name='student_profile'),
    path('staff-profile/', views.StaffProfileView.as_view(), name='staff_profile'),
]