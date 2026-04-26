from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.utils import timezone
from .models import PermissionRequest, SalaryVerification
from .serializers import PermissionRequestSerializer, SalaryVerificationSerializer


class PermissionRequestListView(generics.ListAPIView):
    """List all permission requests"""
    serializer_class = PermissionRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Only Director can view all permission requests
        if self.request.user.role == 'director':
            return PermissionRequest.objects.all()
        return PermissionRequest.objects.none()


class PermissionRequestDetailView(generics.RetrieveUpdateAPIView):
    """Retrieve and update permission request"""
    serializer_class = PermissionRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.role == 'director':
            return PermissionRequest.objects.all()
        return PermissionRequest.objects.none()
    
    def perform_update(self, serializer):
        if self.request.user.role == 'director':
            serializer.save(approved_by=self.request.user, approved_at=timezone.now())


class SalaryVerificationListView(generics.ListAPIView):
    """List all salary verification requests"""
    serializer_class = SalaryVerificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Only Director can view all salary verification requests
        if self.request.user.role == 'director':
            return SalaryVerification.objects.all()
        return SalaryVerification.objects.none()


class SalaryVerificationDetailView(generics.RetrieveUpdateAPIView):
    """Retrieve and update salary verification request"""
    serializer_class = SalaryVerificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.role == 'director':
            return SalaryVerification.objects.all()
        return SalaryVerification.objects.none()
    
    def perform_update(self, serializer):
        if self.request.user.role == 'director':
            serializer.save(processed_by=self.request.user, processed_at=timezone.now())


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def director_dashboard(request):
    """Director dashboard data"""
    if request.user.role != 'director':
        return Response({'error': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
    
    # Get permission request statistics
    total_requests = PermissionRequest.objects.count()
    pending_requests = PermissionRequest.objects.filter(status='pending').count()
    approved_requests = PermissionRequest.objects.filter(status='approved').count()
    rejected_requests = PermissionRequest.objects.filter(status='rejected').count()
    
    # Get salary verification statistics
    total_verifications = SalaryVerification.objects.count()
    pending_verifications = SalaryVerification.objects.filter(status='pending').count()
    
    # Recent activities
    recent_requests = PermissionRequest.objects.order_by('-requested_at')[:5]
    recent_verifications = SalaryVerification.objects.order_by('-requested_at')[:5]
    
    data = {
        'statistics': {
            'permission_requests': {
                'total': total_requests,
                'pending': pending_requests,
                'approved': approved_requests,
                'rejected': rejected_requests,
            },
            'salary_verifications': {
                'total': total_verifications,
                'pending': pending_verifications,
            },
        },
        'recent_activities': {
            'permission_requests': PermissionRequestSerializer(recent_requests, many=True).data,
            'salary_verifications': SalaryVerificationSerializer(recent_verifications, many=True).data,
        },
    }
    
    return Response(data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def approve_permission_request(request, request_id):
    """Approve a permission request"""
    if request.user.role != 'director':
        return Response({'error': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        permission_request = PermissionRequest.objects.get(id=request_id)
    except PermissionRequest.DoesNotExist:
        return Response({'error': 'Permission request not found'}, status=status.HTTP_404_NOT_FOUND)
    
    approval_notes = request.data.get('approval_notes', '')
    
    permission_request.status = 'approved'
    permission_request.approved_by = request.user
    permission_request.approved_at = timezone.now()
    permission_request.approval_notes = approval_notes
    permission_request.save()
    
    return Response({'message': 'Permission request approved successfully'})


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def reject_permission_request(request, request_id):
    """Reject a permission request"""
    if request.user.role != 'director':
        return Response({'error': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        permission_request = PermissionRequest.objects.get(id=request_id)
    except PermissionRequest.DoesNotExist:
        return Response({'error': 'Permission request not found'}, status=status.HTTP_404_NOT_FOUND)
    
    rejection_notes = request.data.get('rejection_notes', '')
    
    permission_request.status = 'rejected'
    permission_request.approved_by = request.user
    permission_request.approved_at = timezone.now()
    permission_request.approval_notes = rejection_notes
    permission_request.save()
    
    return Response({'message': 'Permission request rejected'})