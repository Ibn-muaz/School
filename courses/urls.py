from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.CourseListView.as_view(), name='course_list'),
    path('<int:pk>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('offerings/', views.CourseOfferingListView.as_view(), name='course_offerings'),
    path('catalog/', views.course_catalog, name='course_catalog'),
    path('lecturer-courses/', views.lecturer_courses, name='lecturer_courses'),
]