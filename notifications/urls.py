from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('', views.NotificationListView.as_view(), name='notification_list'),
    path('<int:pk>/', views.NotificationDetailView.as_view(), name='notification_detail'),
    path('templates/', views.NotificationTemplateListView.as_view(), name='notification_templates'),
    path('mark-read/<int:notification_id>/', views.mark_as_read, name='mark_as_read'),
    path('mark-all-read/', views.mark_all_as_read, name='mark_all_read'),
    path('send/', views.send_notification, name='send_notification'),
    path('stats/', views.notification_stats, name='notification_stats'),
]