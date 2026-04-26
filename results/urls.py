from django.urls import path
from . import views

app_name = 'results'

urlpatterns = [
    path('', views.ResultListView.as_view(), name='result_list'),
    path('<int:pk>/', views.ResultDetailView.as_view(), name='result_detail'),
    path('semester/', views.SemesterResultListView.as_view(), name='semester_results'),
    path('dashboard/', views.student_results_dashboard, name='results_dashboard'),
    path('transcripts/', views.TranscriptListCreateView.as_view(), name='transcripts'),
    path('approve/<int:result_id>/', views.approve_result, name='approve_result'),
    path('publish/', views.publish_results, name='publish_results'),
]