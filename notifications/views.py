from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.utils import timezone
from .models import Notification, NotificationTemplate
from .serializers import NotificationSerializer, NotificationTemplateSerializer


class NotificationListView(generics.ListAPIView):
    """List notifications for user"""
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        
        # Get notifications for specific user
        user_notifications = Notification.objects.filter(recipient=user)
        
        # Get role-based notifications
        role_notifications = Notification.objects.filter(recipient_role__in=[user.role, 'all'])
        
        # Combine and remove duplicates
        all_notifications = user_notifications.union(role_notifications)
        
        # Order by creation date
        return all_notifications.order_by('-created_at')


class NotificationDetailView(generics.RetrieveUpdateAPIView):
    """Retrieve and update notification"""
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)
    
    def perform_update(self, serializer):
        # Mark as read when updating
        if not serializer.instance.is_read:
            serializer.save(is_read=True, read_at=timezone.now())
        else:
            serializer.save()


class NotificationTemplateListView(generics.ListAPIView):
    """List notification templates (admin only)"""
    serializer_class = NotificationTemplateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Only ICT Director and Director can view templates
        if self.request.user.role in ['ict_director', 'director']:
            return NotificationTemplate.objects.filter(is_active=True)
        return NotificationTemplate.objects.none()


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def mark_as_read(request, notification_id):
    """Mark notification as read"""
    try:
        notification = Notification.objects.get(
            id=notification_id,
            recipient=request.user
        )
    except Notification.DoesNotExist:
        return Response({'error': 'Notification not found'}, status=status.HTTP_404_NOT_FOUND)
    
    notification.is_read = True
    notification.read_at = timezone.now()
    notification.save()
    
    return Response({'message': 'Notification marked as read'})


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def mark_all_as_read(request):
    """Mark all notifications as read for user"""
    user = request.user
    
    # Update user-specific notifications
    Notification.objects.filter(recipient=user, is_read=False).update(
        is_read=True,
        read_at=timezone.now()
    )
    
    # For role-based notifications, create read records if needed
    # This is a simplified approach - in production, you might want to track reads differently
    
    return Response({'message': 'All notifications marked as read'})


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def send_notification(request):
    """Send notification (admin roles only)"""
    if request.user.role not in ['ict_director', 'director']:
        return Response({'error': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
    
    title = request.data.get('title')
    message = request.data.get('message')
    notification_type = request.data.get('notification_type', 'info')
    priority = request.data.get('priority', 'medium')
    recipient_role = request.data.get('recipient_role')  # 'all', 'student', 'staff', etc.
    recipient_id = request.data.get('recipient_id')  # For specific user
    
    if not title or not message:
        return Response({'error': 'Title and message are required'}, status=status.HTTP_400_BAD_REQUEST)
    
    if recipient_id:
        # Send to specific user
        try:
            from accounts.models import User
            recipient = User.objects.get(id=recipient_id)
            notification = Notification.objects.create(
                title=title,
                message=message,
                notification_type=notification_type,
                priority=priority,
                recipient=recipient,
                sender=request.user
            )
        except User.DoesNotExist:
            return Response({'error': 'Recipient not found'}, status=status.HTTP_404_NOT_FOUND)
    elif recipient_role:
        # Send to role-based recipients
        notification = Notification.objects.create(
            title=title,
            message=message,
            notification_type=notification_type,
            priority=priority,
            recipient_role=recipient_role,
            sender=request.user
        )
    else:
        return Response({'error': 'Either recipient_id or recipient_role must be provided'}, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({
        'message': 'Notification sent successfully',
        'notification_id': notification.id
    })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def notification_stats(request):
    """Get notification statistics"""
    user = request.user
    
    total_notifications = Notification.objects.filter(recipient=user).count()
    unread_notifications = Notification.objects.filter(recipient=user, is_read=False).count()
    
    # Role-based notifications
    role_notifications = Notification.objects.filter(
        recipient_role__in=[user.role, 'all']
    ).exclude(recipient=user)  # Exclude duplicates
    
    total_role_notifications = role_notifications.count()
    unread_role_notifications = role_notifications.filter(is_read=False).count()
    
    return Response({
        'user_notifications': {
            'total': total_notifications,
            'unread': unread_notifications,
        },
        'role_notifications': {
            'total': total_role_notifications,
            'unread': unread_role_notifications,
        },
        'total_unread': unread_notifications + unread_role_notifications,
    })