from django.urls import path
from . import views

app_name = 'fees'

urlpatterns = [
    path('structures/', views.FeeStructureListView.as_view(), name='fee_structures'),
    path('dashboard/', views.student_fees_dashboard, name='fees_dashboard'),
    path('payments/', views.FeePaymentListCreateView.as_view(), name='fee_payments'),
    path('payments/<int:pk>/', views.FeePaymentDetailView.as_view(), name='fee_payment_detail'),
    path('other-payments/', views.OtherPaymentListCreateView.as_view(), name='other_payments'),
    path('initiate-payment/', views.initiate_online_payment, name='initiate_payment'),
    path('verify-payment/', views.verify_payment, name='verify_payment'),
]