"""
Portal security middleware:
  1. AuditMiddleware  — logs POST/PUT/DELETE requests
  2. AccountLockMiddleware — blocks locked accounts
  3. SessionSecurityMiddleware — idle timeout enforcement
"""
from django.utils import timezone
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import logout


class AccountLockMiddleware:
    """Block requests from locked-out accounts."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            user = request.user
            if user.is_locked:
                logout(request)
                messages.error(
                    request,
                    f'Your account is temporarily locked due to multiple failed login attempts. '
                    f'Please try again after {user.account_locked_until.strftime("%H:%M")}.'
                )
                return redirect('portal:login')
        return self.get_response(request)


class SessionSecurityMiddleware:
    """Enforce idle session timeout (20 minutes)."""

    IDLE_TIMEOUT = 20 * 60  # seconds
    EXEMPT_PATHS = ['/login/', '/logout/', '/static/', '/media/', '/api/']

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # Check if path is exempt
            if not any(request.path.startswith(p) for p in self.EXEMPT_PATHS):
                last_activity = request.session.get('last_activity')
                if last_activity:
                    elapsed = (timezone.now().timestamp() - last_activity)
                    if elapsed > self.IDLE_TIMEOUT:
                        logout(request)
                        messages.warning(
                            request,
                            'Your session expired due to inactivity. Please log in again.'
                        )
                        return redirect('portal:login')
                # Update last activity timestamp
                request.session['last_activity'] = timezone.now().timestamp()

        return self.get_response(request)


class AuditMiddleware:
    """Log significant state-changing requests to AuditLog."""

    AUDITED_METHODS = {'POST', 'PUT', 'PATCH', 'DELETE'}
    SKIP_PATHS = ['/static/', '/media/', '/admin/jsi18n/']

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Only log after successful responses for audited methods
        if (
            request.method in self.AUDITED_METHODS
            and request.user.is_authenticated
            and not any(request.path.startswith(p) for p in self.SKIP_PATHS)
            and response.status_code < 500
        ):
            try:
                from ict_director.models import AuditLog
                AuditLog.objects.create(
                    user=request.user,
                    action='OTHER',
                    resource_type='HTTP',
                    resource_id=request.path,
                    ip_address=self._get_ip(request),
                    user_agent=request.META.get('HTTP_USER_AGENT', '')[:500],
                    session_id=request.session.session_key or '',
                    status='success' if response.status_code < 400 else 'failed',
                    details=f'{request.method} {request.path} → {response.status_code}',
                )
            except Exception:
                pass  # Never let audit logging break the app

        return response

    @staticmethod
    def _get_ip(request):
        xff = request.META.get('HTTP_X_FORWARDED_FOR')
        if xff:
            return xff.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR', '127.0.0.1')
