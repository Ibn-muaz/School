from django.urls import path
from . import views

app_name = 'clearance'

urlpatterns = [
    # ── Student Routes ──────────────────────────────────────────────────
    path('', views.clearance_dashboard, name='dashboard'),
    path('pay-acceptance/', views.pay_acceptance_fee, name='pay_acceptance'),
    path('upload-document/', views.upload_clearance_document, name='upload_document'),
    path('delete-document/<int:doc_id>/', views.delete_clearance_document, name='delete_document'),
    path('submit/', views.submit_for_approval, name='submit_for_approval'),

    # ── Staff/Registrar Routes ──────────────────────────────────────────
    path('review/', views.clearance_review_list, name='review_list'),
    path('review/<int:pk>/', views.clearance_review_detail, name='review_detail'),
    path('verify-document/<int:doc_id>/', views.verify_document, name='verify_document'),
    path('approve/<int:pk>/', views.approve_clearance, name='approve'),
    path('reject/<int:pk>/', views.reject_clearance, name='reject'),

    # ── Bursary Routes ──────────────────────────────────────────────────
    path('configure-fee/', views.configure_acceptance_fee, name='configure_fee'),
]
