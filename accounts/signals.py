from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from notifications.models import Notification

@receiver(post_save, sender=User)
def notify_director_new_user(sender, instance, created, **kwargs):
    if created:
        # Avoid circular imports if any, but Notification is in another app
        Notification.objects.create(
            recipient_role='director',
            title='New User Created',
            message=f'A new account has been created: {instance.username} ({instance.get_role_display()})',
            notification_type='info'
        )
