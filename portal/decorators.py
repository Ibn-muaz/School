"""
Portal decorators — RBAC enforcement at the view level.
"""
from functools import wraps
from django.shortcuts import redirect, render
from django.contrib import messages


def login_required_portal(view_func):
    """Ensure the user is authenticated via Django session."""
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Please log in to access this page.')
            return redirect('portal:login')
        return view_func(request, *args, **kwargs)
    return _wrapped


def role_required(*roles):
    """
    Restrict a view to specific roles.
    Usage:
        @role_required('student', 'lecturer')
        def my_view(request): ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.warning(request, 'Please log in to access this page.')
                return redirect('portal:login')
            if request.user.role not in roles:
                return render(request, 'errors/403.html', {
                    'required_roles': roles,
                    'user_role': request.user.role,
                }, status=403)
            return view_func(request, *args, **kwargs)
        return _wrapped
    return decorator


def ict_director_required(view_func):
    """Shortcut decorator — ICT Director only."""
    return role_required('ict_director')(view_func)


def staff_roles_required(view_func):
    """Allow all non-student roles."""
    return role_required(
        'lecturer', 'practical_master',
        'hod', 'hod_coordinator',
        'dean_students_affairs', 'deputy_dean_students_affairs', 'academic_secretary',
        'provost', 'registrar', 'deputy_registrar', 'exams_officer', 'admin_officer',
        'bursary', 'liaison_officer', 'hostel_admin', 'ict_director', 'director'
    )(view_func)
