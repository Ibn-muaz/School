from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Sum
from django.utils import timezone
from .models import FeeStructure, FeePayment, OtherPayment
from .serializers import FeeStructureSerializer, FeePaymentSerializer, OtherPaymentSerializer
from accounts.models import StudentProfile
from accounts.matric_utils import generate_matriculation_number


class FeeStructureListView(generics.ListAPIView):
    """List fee structures"""
    serializer_class = FeeStructureSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return FeeStructure.objects.filter(is_active=True)


class FeePaymentListCreateView(generics.ListCreateAPIView):
    """List and create fee payments"""
    serializer_class = FeePaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return FeePayment.objects.filter(student=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(student=self.request.user)


class FeePaymentDetailView(generics.RetrieveAPIView):
    """Retrieve fee payment details"""
    serializer_class = FeePaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return FeePayment.objects.filter(student=self.request.user)


class OtherPaymentListCreateView(generics.ListCreateAPIView):
    """List and create other payments"""
    serializer_class = OtherPaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return OtherPayment.objects.filter(student=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(student=self.request.user)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def student_fees_dashboard(request):
    """Student fees dashboard"""
    user = request.user
    
    try:
        profile = user.student_profile
    except:
        return Response({'error': 'Student profile not found'}, status=400)
    
    # Get current fee structure
    try:
        fee_structure = FeeStructure.objects.get(
            level=profile.level,
            program=profile.department_code,
            academic_year='2023/2024',  # This should be configurable
            is_active=True
        )
    except FeeStructure.DoesNotExist:
        return Response({'error': 'Fee structure not found for your level/program'}, status=404)
    
    # Get total payments made
    total_paid = FeePayment.objects.filter(
        student=user,
        status='completed'
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    # Get payment history
    payment_history = FeePayment.objects.filter(
        student=user
    ).order_by('-payment_date')[:10]
    
    # Calculate outstanding balance
    outstanding_balance = fee_structure.total_fee - total_paid
    
    data = {
        'fee_structure': FeeStructureSerializer(fee_structure).data,
        'payment_summary': {
            'total_fee': fee_structure.total_fee,
            'total_paid': total_paid,
            'outstanding_balance': outstanding_balance,
            'payment_percentage': (total_paid / fee_structure.total_fee * 100) if fee_structure.total_fee > 0 else 0,
        },
        'payment_history': FeePaymentSerializer(payment_history, many=True).data,
    }
    
    return Response(data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def initiate_online_payment(request):
    """Initiate online payment for fees"""
    user = request.user
    amount = request.data.get('amount')
    purpose = request.data.get('purpose', 'tuition_fee')
    
    if not amount:
        return Response({'error': 'Amount is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Generate transaction reference
    import uuid
    transaction_ref = str(uuid.uuid4())[:20].upper()
    
    # Create pending payment record
    payment = FeePayment.objects.create(
        student=user,
        amount=amount,
        payment_method='online',
        transaction_reference=transaction_ref,
        purpose=purpose,
        status='pending'
    )
    
    # TODO: Integrate with payment gateway (Paystack, Flutterwave, etc.)
    # For now, return payment details
    
    return Response({
        'payment_id': payment.id,
        'transaction_reference': transaction_ref,
        'amount': amount,
        'status': 'pending',
        'message': 'Payment initiated. Complete payment using the reference.',
        # In production, this would include payment gateway redirect URL
    })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def verify_payment(request):
    """Verify payment status and assign matriculation number if needed"""
    transaction_ref = request.data.get('transaction_reference')
    
    if not transaction_ref:
        return Response({'error': 'Transaction reference is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        payment = FeePayment.objects.get(transaction_reference=transaction_ref)
    except FeePayment.DoesNotExist:
        return Response({'error': 'Payment not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # TODO: Verify with payment gateway
    # For now, just mark as completed
    
    if payment.status == 'pending':
        payment.status = 'completed'
        payment.verified_by = request.user
        payment.verified_at = timezone.now()
        payment.save()
        
        # Get or create student profile with matriculation number
        try:
            profile = payment.student.student_profile
            # Update total fees paid
            profile.total_fees_paid += payment.amount
            profile.save(update_fields=['total_fees_paid'])
        except StudentProfile.DoesNotExist:
            # If StudentProfile doesn't exist, create it with matriculation number
            try:
                # Get department from application or use a default
                from admissions.models import ApplicationRecord
                application = ApplicationRecord.objects.filter(
                    user=payment.student,
                    status__in=['admitted', 'paid']
                ).first()
                
                department = None
                if application:
                    department = application.first_choice_program
                
                # Generate matriculation number if department is known
                if department:
                    matric = generate_matriculation_number(
                        department=department,
                        academic_year='2025/2026'
                    )
                else:
                    matric = None
                
                # Create StudentProfile with matric number (if available)
                profile_defaults = {
                    'level': '100',
                    'admission_year': timezone.now().year,
                    'total_fees_paid': payment.amount,
                }
                
                if matric:
                    profile_defaults['matriculation_number'] = matric
                    profile_defaults['department_code'] = department
                    # We should probably lookup the full department name too
                    dept_map = dict(StudentProfile.DEPT_CHOICES)
                    profile_defaults['department'] = dept_map.get(department, department)
                
                profile = StudentProfile.objects.create(
                    user=payment.student,
                    **profile_defaults
                )
                
            except Exception as e:
                # Log error but don't fail the payment verification
                print(f"Error creating StudentProfile: {str(e)}")
    
    return Response({
        'payment_id': payment.id,
        'status': payment.status,
        'amount': payment.amount,
        'verified_at': payment.verified_at,
    })