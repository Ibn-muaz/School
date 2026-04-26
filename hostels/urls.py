from django.urls import path
from . import views

app_name = 'hostels'

urlpatterns = [
    # ── Student ──────────────────────────────────────────
    path('', views.student_hostel_dashboard, name='student_dashboard'),
    path('apply/', views.apply_for_bed, name='apply_allocation'),
    path('cancel/<int:allocation_id>/', views.cancel_my_allocation, name='cancel_allocation'),

    # ── Admin / Staff ─────────────────────────────────────
    path('admin/', views.admin_hostel_dashboard, name='admin_dashboard'),
    path('admin/confirm/<int:allocation_id>/', views.admin_confirm_payment, name='confirm_payment'),
    path('admin/cancel/<int:allocation_id>/', views.admin_cancel_allocation, name='admin_cancel'),
]
