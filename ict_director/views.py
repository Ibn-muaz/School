from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from accounts.models import User
from .models import OTPRecord
from .serializers import OTPRecordSerializer


class OTPRecordListView(generics.ListAPIView):
    """List OTP records"""
    serializer_class = OTPRecordSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Only ICT Director can view all OTP records
        if self.request.user.role == 'ict_director':
            return OTPRecord.objects.all()
        return OTPRecord.objects.none()


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def ict_director_dashboard(request):
    """ICT Director dashboard data"""
    if request.user.role != 'ict_director':
        return Response({'error': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
    
    # Get OTP statistics
    today = timezone.now().date()
    last_30_days = timezone.now() - timedelta(days=30)
    
    total_otps = OTPRecord.objects.count()
    todays_otps = OTPRecord.objects.filter(generated_at__date=today).count()
    active_otps = OTPRecord.objects.filter(status='generated', expires_at__gt=timezone.now()).count()
    expired_otps = OTPRecord.objects.filter(status='expired').count()
    
    # Recent OTP activity
    recent_otps = OTPRecord.objects.order_by('-generated_at')[:10]
    
    data = {
        'statistics': {
            'total_otps': total_otps,
            'todays_otps': todays_otps,
            'active_otps': active_otps,
            'expired_otps': expired_otps,
        },
        'recent_activity': OTPRecordSerializer(recent_otps, many=True).data,
    }
    
    return Response(data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def generate_otp(request):
    """Generate OTP for a user"""
    if request.user.role != 'ict_director':
        return Response({'error': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
    
    user_id = request.data.get('user_id')
    purpose = request.data.get('purpose', 'verification')
    
    try:
        target_user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Generate OTP code (6 digits)
    import random
    otp_code = str(random.randint(100000, 999999))
    
    # Set expiry time (10 minutes from now)
    expires_at = timezone.now() + timedelta(minutes=10)
    
    # Create OTP record
    otp_record = OTPRecord.objects.create(
        user=target_user,
        otp_code=otp_code,
        purpose=purpose,
        expires_at=expires_at,
        ip_address=request.META.get('REMOTE_ADDR'),
        user_agent=request.META.get('HTTP_USER_AGENT', ''),
    )
    
    # TODO: Send OTP via email/SMS
    # For now, just return the OTP (in production, this should not be returned)
    
    return Response({
        'message': 'OTP generated successfully',
        'otp_id': otp_record.id,
        'expires_at': otp_record.expires_at,
        # Remove this line in production
        'otp_code': otp_code,
    })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def reset_user_otp(request):
    """Reset OTP for a user (invalidate all active OTPs)"""
    if request.user.role != 'ict_director':
        return Response({'error': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
    
    user_id = request.data.get('user_id')
    
    try:
        target_user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Mark all active OTPs as expired
    active_otps = OTPRecord.objects.filter(
        user=target_user,
        status='generated',
        expires_at__gt=timezone.now()
    )
    
    updated_count = active_otps.update(status='expired')
    
    return Response({
        'message': f'Successfully reset {updated_count} active OTPs for user {target_user.username}'
    })