from django.utils import timezone
from ict_director.models import AuditLog

def _get_client_ip(request):
    xff = request.META.get('HTTP_X_FORWARDED_FOR')
    if xff:
        return xff.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', '127.0.0.1')

def _audit(request, action, resource_type='', resource_id='',
           old_value=None, new_value=None, status='success', details=''):
    try:
        AuditLog.objects.create(
            user=request.user if request.user and request.user.is_authenticated else None,
            action=action,
            resource_type=resource_type,
            resource_id=str(resource_id),
            old_value=old_value,
            new_value=new_value,
            ip_address=_get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')[:500],
            session_id=getattr(request.session, 'session_key', '') or '',
            status=status,
            details=details,
        )
    except Exception:
        pass
