"""
Portal context processors — inject college branding, role info,
notifications, and theme into every template across YCHST portal.
"""
from django.db.models import Q
from django.conf import settings
from notifications.models import Notification


def portal_context(request):
    """Inject common context variables into every template."""

    COLLEGE_NAME = getattr(settings, 'COLLEGE_NAME', "Yar'yaya College of Health Science and Technology")
    COLLEGE_SHORT_NAME = getattr(settings, 'COLLEGE_SHORT_NAME', 'YCHST')
    COLLEGE_MOTTO = getattr(settings, 'COLLEGE_MOTTO', 'Empowering the next generation of health professionals')
    COLLEGE_FULL_NAME = getattr(settings, 'COLLEGE_FULL_NAME', "Yar'yaya College of Health Science and Technology, Sanga")
    CURRENT_ACADEMIC_YEAR = getattr(settings, 'CURRENT_ACADEMIC_YEAR', '2025/2026')

    DEPARTMENTS = getattr(settings, 'DEPARTMENTS', {
        'PHT':  'Public Health Technology',
        'HIMT': 'Health Information Management Technology',
        'CHEW': 'Community Health Extension Workers',
        'PT':   'Pharmacy Technician',
        'MLT':  'Medical Laboratory Technician',
    })

    context = {
        # College branding (available in ALL templates via {{ college_name }})
        'college_name': COLLEGE_NAME,
        'college_short_name': COLLEGE_SHORT_NAME,
        'college_motto': COLLEGE_MOTTO,
        'college_full_name': COLLEGE_FULL_NAME,
        'current_academic_year': CURRENT_ACADEMIC_YEAR,
        'departments': DEPARTMENTS,

        # Notification defaults
        'unread_notifications': [],
        'unread_count': 0,

        # Role display defaults
        'user_role_display': '',
        'user_role_badge_color': 'blue',
        'user_theme': 'light',

        # Grading system info
        'grading_info': {
            'HIMT': 5.0,
            'PHT': 4.0, 'CHEW': 4.0, 'PT': 4.0, 'MLT': 4.0,
        },

        # Role → Sidebar template mapping (strict role-based sidebar)
        'ROLE_SIDEBAR_MAP': {
            'student':                    'partials/sidebar_student.html',
            'applicant':                  'partials/sidebar_applicant.html',
            'lecturer':                   'partials/sidebar_lecturer.html',
            'practical_master':           'partials/sidebar_lecturer.html',
            'hod':                        'partials/sidebar_hod.html',
            'hod_coordinator':            'partials/sidebar_hod.html',
            'dean_students_affairs':      'partials/sidebar_dean_students_affairs.html',
            'deputy_dean_students_affairs': 'partials/sidebar_dean_students_affairs.html',
            'academic_secretary':         'partials/sidebar_admin.html',
            'provost':                    'partials/sidebar_executive.html',
            'registrar':                  'partials/sidebar_registrar.html',
            'deputy_registrar':           'partials/sidebar_registrar.html',
            'exams_officer':              'partials/sidebar_exams.html',
            'admin_officer':              'partials/sidebar_admin.html',
            'bursary':                    'partials/sidebar_bursary.html',
            'liaison_officer':            'partials/sidebar_admin.html',
            'hostel_admin':               'partials/sidebar_hostel.html',
            'ict_director':               'partials/sidebar_ict.html',
            'director':                   'partials/sidebar_executive.html',
        },
    }

    if request.user.is_authenticated:
        user = request.user
        context['user_role_display'] = user.get_role_display()
        context['user_role_badge_color'] = user.get_role_badge_color()
        context['user_theme'] = user.theme_preference
        context['current_sidebar'] = context['ROLE_SIDEBAR_MAP'].get(
            user.role, 'partials/sidebar_student.html'
        )
        # Students use a dedicated base template; staff use the standard one
        context['base_template'] = 'base_student.html' if user.role == 'student' else 'base.html'

        # ── Notifications ──────────────────────────────────────────────────
        try:
            notif_qs = Notification.objects.filter(is_read=False).filter(
                Q(recipient=user) | Q(recipient_role=user.role) | Q(recipient_role='all')
            ).order_by('-created_at')
            context['unread_notifications'] = list(notif_qs[:5])
            context['unread_count'] = notif_qs.count()
        except Exception:
            pass

        # ── Pending admissions count for Registrar ─────────────────────────
        try:
            if user.role in ('registrar', 'deputy_registrar', 'director', 'provost'):
                from admissions.models import ApplicationRecord
                context['pending_admissions_count'] = ApplicationRecord.objects.filter(
                    status='submitted'
                ).count()
        except Exception:
            pass

    return context
