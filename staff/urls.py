from django.urls import path
from . import views

app_name = 'staff'

urlpatterns = [
    path('dashboard/', views.staff_dashboard, name='dashboard'),
    path('course-allocations/', views.CourseAllocationListView.as_view(), name='course_allocations'),
    path('scoresheets/', views.ScoresheetListCreateView.as_view(), name='scoresheets_list'),
    path('scoresheets/<int:pk>/', views.ScoresheetDetailView.as_view(), name='scoresheets_detail'),
    path('salary-records/', views.SalaryRecordListView.as_view(), name='salary_records'),
]