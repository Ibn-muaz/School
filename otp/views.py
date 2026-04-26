from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
import random
from .models import OTPSettings, OTPAttempt, OTPBlacklist
from .serializers import OTPSettingsSerializer, OTPAttemptSerializer


class OTPSettingsView(generics.RetrieveUpdateAPIView):
    """OTP settings view"""
    serializer_class = OTPSettingsSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        # Get or create OTP settings for user
        settings, created = OTPSettings.objects.get_or_create(user=self.request.user)
        return settings


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def verify_otp(request):
    """Verify OTP code"""
    otp_code = request.data.get('otp_code')
    purpose = request.data.get('purpose', 'verification')
    
    if not otp_code:
        return Response({'error': 'OTP code is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = request.user
    
    # Check if OTP is blacklisted
    if OTPBlacklist.objects.filter(otp_code=otp_code).exists():
        # Log failed attempt
        OTPAttempt.objects.create(
            user=user,
            otp_code=otp_code,
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            status='failed'
        )
        return Response({'error': 'Invalid OTP code'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Import OTPRecord from ict_director app
    from ict_director.models import OTPRecord
    
    try:
        otp_record = OTPRecord.objects.get(
            user=user,
            otp_code=otp_code,
            purpose=purpose,
            status='generated'
        )
        
        # Check if OTP is expired
        if otp_record.is_expired():
            otp_record.status = 'expired'
            otp_record.save()
            
            # Log failed attempt
            OTPAttempt.objects.create(
                user=user,
                otp_code=otp_code,
                ip_address=request.META.get('REMOTE_ADDR'),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                status='expired'
            )
            
            return Response({'error': 'OTP has expired'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Mark OTP as used
        otp_record.status = 'used'
        otp_record.used_at = timezone.now()
        otp_record.save()
        
        # Log successful attempt
        OTPAttempt.objects.create(
            user=user,
            otp_code=otp_code,
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            status='success'
        )
        
        # Update user OTP verification status
        if purpose == 'verification':
            user.is_otp_verified = True
            user.save()
        
        return Response({
            'message': 'OTP verified successfully',
            'purpose': purpose
        })
        
    except OTPRecord.DoesNotExist:
        # Log failed attempt
        OTPAttempt.objects.create(
            user=user,
            otp_code=otp_code,
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            status='failed'
        )
        
        return Response({'error': 'Invalid OTP code'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def request_otp(request):
    """Request new OTP"""
    purpose = request.data.get('purpose', 'verification')
    delivery_method = request.data.get('delivery_method', 'email')  # email or sms
    
    user = request.user
    
    # Get or create OTP settings
    settings, created = OTPSettings.objects.get_or_create(user=user)
    
    # Check if user has exceeded max attempts (simplified check)
    recent_attempts = OTPAttempt.objects.filter(
        user=user,
        attempted_at__gte=timezone.now() - timedelta(minutes=settings.lockout_duration_minutes)
    ).count()
    
    if recent_attempts >= settings.max_attempts:
        return Response({
            'error': f'Too many attempts. Try again after {settings.lockout_duration_minutes} minutes'
        }, status=status.HTTP_429_TOO_MANY_REQUESTS)
    
    # Generate OTP
    otp_code = str(random.randint(100000, 999999))
    
    # Create OTP record
    from ict_director.models import OTPRecord
    otp_record = OTPRecord.objects.create(
        user=user,
        otp_code=otp_code,
        purpose=purpose,
        expires_at=timezone.now() + timedelta(minutes=settings.otp_expiry_minutes),
        ip_address=request.META.get('REMOTE_ADDR'),
        user_agent=request.META.get('HTTP_USER_AGENT', ''),
    )
    
    # TODO: Send OTP via email or SMS
    # For now, just return success (in production, implement actual sending)
    
    return Response({
        'message': f'OTP sent successfully via {delivery_method}',
        'expires_in_minutes': settings.otp_expiry_minutes,
        # Remove this in production
        'otp_code': otp_code,
    })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def blacklist_otp(request):
    """Blacklist an OTP (admin only)"""
    if request.user.role not in ['ict_director', 'director']:
        return Response({'error': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
    
    otp_code = request.data.get('otp_code')
    reason = request.data.get('reason', 'Compromised')
    
    if not otp_code:
        return Response({'error': 'OTP code is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if already blacklisted
    if OTPBlacklist.objects.filter(otp_code=otp_code).exists():
        return Response({'error': 'OTP code is already blacklisted'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Create blacklist entry
    blacklist_entry = OTPBlacklist.objects.create(
        otp_code=otp_code,
        reason=reason,
        blacklisted_by=request.user,
        expires_at=timezone.now() + timedelta(days=30)  # Blacklist for 30 days
    )
    
    return Response({
        'message': 'OTP code blacklisted successfully',
        'blacklist_id': blacklist_entry.id
    })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def otp_stats(request):
    """Get OTP statistics"""
    if request.user.role not in ['ict_director', 'director']:
        return Response({'error': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
    
    # Get OTP statistics
    from ict_director.models import OTPRecord
    
    total_otps = OTPRecord.objects.count()
    active_otps = OTPRecord.objects.filter(status='generated', expires_at__gt=timezone.now()).count()
    used_otps = OTPRecord.objects.filter(status='used').count()
    expired_otps = OTPRecord.objects.filter(status='expired').count()
    
    # Recent attempts
    recent_attempts = OTPAttempt.objects.order_by('-attempted_at')[:10]
    
    return Response({
        'statistics': {
            'total_otps': total_otps,
            'active_otps': active_otps,
            'used_otps': used_otps,
            'expired_otps': expired_otps,
        },
        'recent_attempts': OTPAttemptSerializer(recent_attempts, many=True).data,
    })