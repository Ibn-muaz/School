from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path('dashboard/', views.student_dashboard, name='dashboard'),
    path('course-registration/', views.CourseRegistrationListCreateView.as_view(), name='course_registration_list'),
    path('course-registration/<int:pk>/', views.CourseRegistrationDetailView.as_view(), name='course_registration_detail'),
    path('program-change/', views.ProgramChangeListCreateView.as_view(), name='program_change_list'),
    path('program-change/<int:pk>/', views.ProgramChangeDetailView.as_view(), name='program_change_detail'),
    path('indexing/', views.IndexingRequestListCreateView.as_view(), name='indexing_list'),
    path('indexing/<int:pk>/', views.IndexingRequestDetailView.as_view(), name='indexing_detail'),
]