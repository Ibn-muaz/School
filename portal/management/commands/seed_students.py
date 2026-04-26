"""
Management command: seed_students
Populates all 92 enrolled students for YCHST Sanga (2025/2026 session)
organized by department with official matric numbers.

Usage:
    python manage.py seed_students
    python manage.py seed_students --clear   (wipe first, then reseed)
"""

from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils import timezone


# ─── Official Student Register ─────────────────────────────────────────────
STUDENT_DATA = {
    'PHT': {
        'name': 'Public Health Technology',
        'students': [
            (1,  'NUSAIBA MURTALA',            'YCHST/2025/2026/PHT/001'),
            (2,  'UGWU KINGSLEY CHINONSO',      'YCHST/2025/2026/PHT/002'),
            (3,  'LUCY ADAMU',                  'YCHST/2025/2026/PHT/003'),
            (4,  'ABDULLAHI SHAMSUDEEN',        'YCHST/2025/2026/PHT/004'),
            (5,  'CHRISTIANA HABILA',           'YCHST/2025/2026/PHT/005'),
            (6,  'JIBRIN AMINA',                'YCHST/2025/2026/PHT/006'),
            (7,  'UMAR FATIMA',                 'YCHST/2025/2026/PHT/007'),
            (8,  'SULEIMAN HAJARA',             'YCHST/2025/2026/PHT/008'),
            (9,  'BILKISU MUSA',                'YCHST/2025/2026/PHT/009'),
            (10, 'MUKAILU FATIMA',              'YCHST/2025/2026/PHT/010'),
            (11, "ZAKARI SHA'AWANATU",          'YCHST/2025/2026/PHT/011'),
            (12, "SA'ADATU MUHAMMED",           'YCHST/2025/2026/PHT/012'),
            (13, 'ERNEST DANIEL',               'YCHST/2025/2026/PHT/013'),
            (14, 'BILKISU M. SALEH',            'YCHST/2025/2026/PHT/014'),
            (15, 'FAIZA IBRAHIM',               'YCHST/2025/2026/PHT/015'),
            (16, 'ADAMU AISHA ABANNI',          'YCHST/2025/2026/PHT/016'),
            (17, "BENJAMIN NA'OMI",             'YCHST/2025/2026/PHT/017'),
        ]
    },
    'HIMT': {
        'name': 'Health Information Management Technology',
        'students': [
            (1,  'ZUBAIRU AHMED MOHAMMED',      'YCHST/2025/2026/HIMT/001'),
            (2,  'DANLADI HAUWA',               'YCHST/2025/2026/HIMT/002'),
            (3,  'UBANDOMA LOIS',               'YCHST/2025/2026/HIMT/003'),
            (4,  'GOODNESS LUKA',               'YCHST/2025/2026/HIMT/004'),
            (5,  'SALIM ABDULLAHI',             'YCHST/2025/2026/HIMT/005'),
            (6,  'TANIMU DAUDA',                'YCHST/2025/2026/HIMT/006'),
            (7,  'ABUBAKAR KHALIFA YUSUF',      'YCHST/2025/2026/HIMT/007'),
            (8,  'PRECIOUS VIVIAN',             'YCHST/2025/2026/HIMT/008'),
            (9,  'HABIBA ABDULLAHI',            'YCHST/2025/2026/HIMT/009'),
            (10, 'KABIRU YAKUBU',               'YCHST/2025/2026/HIMT/010'),
        ]
    },
    'CHEW': {
        'name': 'Community Health Extension Workers',
        'students': [
            (1,  'YUSUF JIBRIN',               'YCHST/2025/2026/CHEW/001'),
            (2,  'ABDULLAHI MARYAM',            'YCHST/2025/2026/CHEW/002'),
            (3,  'USMAN MARYAM',                'YCHST/2025/2026/CHEW/003'),
            (4,  'ZUBAIDA IBRAHIM',             'YCHST/2025/2026/CHEW/004'),
            (5,  'FATIMA ABDULLAHI',            'YCHST/2025/2026/CHEW/005'),
            (6,  'HARIRA SULEIMAN YAMUSA',      'YCHST/2025/2026/CHEW/006'),
            (7,  'PAULINA BENJAMIN',            'YCHST/2025/2026/CHEW/007'),
            (8,  'FATIMA ALIYU ZAKARI',         'YCHST/2025/2026/CHEW/008'),
            (9,  'BLESSED ZAKKA',               'YCHST/2025/2026/CHEW/009'),
            (10, 'SOLOMON DESTINY',             'YCHST/2025/2026/CHEW/010'),
            (11, 'FATIMA ALIYU',                'YCHST/2025/2026/CHEW/011'),
            (12, 'SALAMATU IDRIS',              'YCHST/2025/2026/CHEW/012'),
            (13, 'SALISU BILKISU',              'YCHST/2025/2026/CHEW/013'),
            (14, 'UMMULKHAIRI JIBRIL',          'YCHST/2025/2026/CHEW/014'),
            (15, 'COMFORT NICOLAS',             'YCHST/2025/2026/CHEW/015'),
            (16, 'ABAMU BULUS',                 'YCHST/2025/2026/CHEW/016'),
            (17, 'YUSIRA IBRAHIM',              'YCHST/2025/2026/CHEW/017'),
            (18, 'HAUWA ADAMU',                 'YCHST/2025/2026/CHEW/018'),
            (19, 'FORBEARANCE PETER',           'YCHST/2025/2026/CHEW/019'),
            (20, 'BALA FAITH YAKUBU',           'YCHST/2025/2026/CHEW/020'),
            (21, 'KHADIJA ISIYA',               'YCHST/2025/2026/CHEW/021'),
            (22, 'SALOMI ISHAYA',               'YCHST/2025/2026/CHEW/022'),
            (23, 'ALHERI AMBI',                 'YCHST/2025/2026/CHEW/023'),
            (24, 'MARKUS VALENTINA',            'YCHST/2025/2026/CHEW/024'),
            (25, 'HAJARA MOHAMMED',             'YCHST/2025/2026/CHEW/025'),
            (26, 'ABUBAKAR AISHA',              'YCHST/2025/2026/CHEW/026'),
            (27, 'BULUS MANZO',                 'YCHST/2025/2026/CHEW/027'),
            (28, 'DORATHY JOEL',                'YCHST/2025/2026/CHEW/028'),
            (29, 'MATHIAS SAMUEL',              'YCHST/2025/2026/CHEW/029'),
        ]
    },
    'PT': {
        'name': 'Pharmacy Technician',
        'students': [
            (1,  'HAPPY NICHOLAS',              'YCHST/2025/2026/PT/001'),
            (2,  'GIMSON EZEKIEL',              'YCHST/2025/2026/PT/002'),
            (3,  'LAWAL MUHAMMADU SANI',        'YCHST/2025/2026/PT/003'),
            (4,  "ZULFA'U SALLAU BABALE",       'YCHST/2025/2026/PT/004'),
            (5,  'ABDULLAHI YUSUF AHMED',       'YCHST/2025/2026/PT/005'),
            (6,  "FATIMA MU'AZU",               'YCHST/2025/2026/PT/006'),
            (7,  'MUHIBBAT YUSUF',              'YCHST/2025/2026/PT/007'),
            (8,  'SALISU AMINU',                'YCHST/2025/2026/PT/008'),
            (9,  'KABIRU AHMED',                'YCHST/2025/2026/PT/009'),
            (10, 'HUSNAT MOHAMMED LAWAL',       'YCHST/2025/2026/PT/010'),
            (11, 'IDRIS NAFISAT ADAM',          'YCHST/2025/2026/PT/011'),
            (12, 'NANA KHADIJA ABDULLAHI',      'YCHST/2025/2026/PT/012'),
            (13, 'ELIJAH MATHEW',               'YCHST/2025/2026/PT/013'),
            (14, 'ISAAC BENJAMIN',              'YCHST/2025/2026/PT/014'),
            (15, 'MUSA MOHAMMED',               'YCHST/2025/2026/PT/015'),
            (16, 'FATIMA MOHAMMED',             'YCHST/2025/2026/PT/016'),
            (17, 'IDRIS ADAM',                  'YCHST/2025/2026/PT/017'),
            (18, 'ASIYA DAUDA',                 'YCHST/2025/2026/PT/018'),
            (19, 'MARYAM SHUAIBU',              'YCHST/2025/2026/PT/019'),
            (20, 'FAITH ADAMU JOSEPH',          'YCHST/2025/2026/PT/020'),
            (21, 'RILWAN ADAMU',                'YCHST/2025/2026/PT/021'),
        ]
    },
    'MLT': {
        'name': 'Medical Laboratory Technician',
        'students': [
            (1,  'UMAR MUHAMMED',               'YCHST/2025/2026/MLT/001'),
            (2,  'MUSA BALARABE',               'YCHST/2025/2026/MLT/002'),
            (3,  'MARYAM KASIMU BABA',          'YCHST/2025/2026/MLT/003'),
            (4,  "SA'ADATU YA'U SULEIMAN",      'YCHST/2025/2026/MLT/004'),
            (5,  'BILYA AISHA MUSA',            'YCHST/2025/2026/MLT/005'),
            (6,  "HADIZA RABI'U",               'YCHST/2025/2026/MLT/006'),
            (7,  'KHADIJATU SANI',              'YCHST/2025/2026/MLT/007'),
            (8,  'RABECCA UBANDOMA',            'YCHST/2025/2026/MLT/008'),
            (9,  'GIMSON EZRA',                 'YCHST/2025/2026/MLT/009'),
            (10, 'ADAMA IDRIS ISIYAKU',         'YCHST/2025/2026/MLT/010'),
            (11, 'ISRAEL BENJAMIN',             'YCHST/2025/2026/MLT/011'),
            (12, 'JOHN LOIS',                   'YCHST/2025/2026/MLT/012'),
            (13, 'MUHAMMAD ANAS',               'YCHST/2025/2026/MLT/013'),
            (14, 'ALIYU UMMULKHAISI',           'YCHST/2025/2026/MLT/014'),
            (15, 'HAFSAT AKIBU',                'YCHST/2025/2026/MLT/015'),
        ]
    },
}

# ─── Staff Accounts ─────────────────────────────────────────────────────────
STAFF_DATA = [
    # role,                    username,        first_name,         last_name,            staff_id,     staff_dept,    is_super
    ('director',               'director',      'Director',         'YCHST',              'YCHST-DIR-001','',          True),
    ('provost',                'provost',       'Provost',          'YCHST',              'YCHST-PRV-001','',          False),
    ('registrar',              'registrar',     'Registrar',        'YCHST',              'YCHST-REG-001','',          False),
    ('deputy_registrar',       'dep_registrar', 'Deputy',           'Registrar',          'YCHST-DRG-001','',          False),
    ('admin_officer',          'admin_officer', 'Admin',            'Officer',            'YCHST-ADM-001','',          False),
    ('bursary',                'bursar',        'Bursar',           'YCHST',              'YCHST-BUR-001','',          False),
    ('dean_students_affairs',  'dean_sa',       'Dean',             'Students Affairs',   'YCHST-DSA-001','',          False),
    ('deputy_dean_students_affairs', 'dep_dean','Deputy Dean',      'Students Affairs',   'YCHST-DDA-001','',          False),
    ('academic_secretary',     'acad_sec',      'Academic',         'Secretary',          'YCHST-ACS-001','',          False),
    ('practical_master',       'prac_master',   'Practical',        'Master',             'YCHST-PM-001', '',          False),
    ('liaison_officer',        'liaison',       'Liaison',          'Officer',            'YCHST-LO-001', '',          False),
    ('ict_director',           'ict_director',  'ICT',              'Director',           'YCHST-ICT-001','',          True),
    # HODs per department
    ('hod',                    'hod_pht',       'HOD',              'Pub Health Tech',    'YCHST-HOD-PHT','PHT',       False),
    ('hod',                    'hod_himt',      'HOD',              'Health Info Mgmt',   'YCHST-HOD-HIMT','HIMT',    False),
    ('hod',                    'hod_chew',      'HOD',              'Community Health',   'YCHST-HOD-CHEW','CHEW',    False),
    ('hod',                    'hod_pt',        'HOD',              'Pharmacy Tech',      'YCHST-HOD-PT', 'PT',        False),
    ('hod',                    'hod_mlt',       'HOD',              'Medical Lab Tech',   'YCHST-HOD-MLT','MLT',      False),
    # Coordinators
    ('hod_coordinator',        'coord_pht',     'Coordinator',      'PHT',                'YCHST-CRD-PHT','PHT',      False),
    ('hod_coordinator',        'coord_himt',    'Coordinator',      'HIMT',               'YCHST-CRD-HIMT','HIMT',   False),
    ('hod_coordinator',        'coord_chew',    'Coordinator',      'CHEW',               'YCHST-CRD-CHEW','CHEW',   False),
    ('hod_coordinator',        'coord_pt',      'Coordinator',      'PT',                 'YCHST-CRD-PT', 'PT',       False),
    ('hod_coordinator',        'coord_mlt',     'Coordinator',      'MLT',                'YCHST-CRD-MLT','MLT',     False),
]


def split_name(full_name):
    """Split full name into first and last name."""
    parts = full_name.strip().split()
    if len(parts) == 1:
        return parts[0].title(), ''
    return parts[0].title(), ' '.join(parts[1:]).title()


class Command(BaseCommand):
    help = "Seed all YCHST Sanga students and staff accounts for 2025/2026 session"

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Delete all existing student accounts before seeding',
        )

    def handle(self, *args, **options):
        from django.contrib.auth import get_user_model
        from accounts.models import StudentProfile, StaffProfile

        User = get_user_model()
        DEFAULT_PW = getattr(settings, 'DEFAULT_STUDENT_PASSWORD', '12345678')
        COLLEGE_NAME = getattr(settings, 'COLLEGE_NAME', "Yar'yaya College of Health Science and Technology")

        if options['clear']:
            self.stdout.write(self.style.WARNING('Clearing existing student accounts...'))
            User.objects.filter(role='student').delete()
            self.stdout.write(self.style.SUCCESS('Student accounts cleared.'))

        self.stdout.write(self.style.MIGRATE_HEADING(
            f"\n{'='*60}\n  YCHST Sanga — Student & Staff Database Seeder\n{'='*60}"
        ))

        # ── 1. Seed Students ───────────────────────────────────────────────
        total_created = 0
        total_existing = 0

        for dept_code, dept_data in STUDENT_DATA.items():
            dept_name = dept_data['name']
            self.stdout.write(f"\n  {dept_code} — {dept_name}")
            self.stdout.write(f"  {'-'*50}")

            for sn, full_name, matric in dept_data['students']:
                first_name, last_name = split_name(full_name)

                # Username = matric number (stored as-is; login view normalizes)
                username = matric  # e.g. YCHST/2025/2026/PHT/001
                email = f"{matric.lower().replace('/', '.').replace('ychst.', '')}@ychst.edu.ng"

                existing = User.objects.filter(username=username).first()
                if existing:
                    self.stdout.write(f"    [EXISTS] {matric} - {full_name}")
                    total_existing += 1
                    continue

                # Create user
                user = User(
                    username=username,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    role='student',
                    must_change_password=True,  # Force password change on first login
                    is_staff=False,
                    is_superuser=False,
                    is_active=True,
                )
                user.set_password(DEFAULT_PW)
                user.save()

                # Create student profile
                StudentProfile.objects.create(
                    user=user,
                    matriculation_number=matric,
                    department_code=dept_code,
                    department=dept_name,
                    level='100',
                    academic_year='2025/2026',
                    admission_year=2025,
                    is_active=True,
                    profile_completed=False,  # Student must complete biodata
                )

                self.stdout.write(
                    self.style.SUCCESS(f"    [OK] {matric}  |  {full_name}")
                )
                total_created += 1

        # ── 2. Seed Staff ──────────────────────────────────────────────────
        self.stdout.write(self.style.MIGRATE_HEADING(f"\n{'='*60}\n  Seeding Staff & Administrative Roles\n{'='*60}"))
        staff_created = 0
        DEPT_NAMES = {
            'PHT':  'Public Health Technology',
            'HIMT': 'Health Information Management Technology',
            'CHEW': 'Community Health Extension Workers',
            'PT':   'Pharmacy Technician',
            'MLT':  'Medical Laboratory Technician',
            '':     'Administration',
        }

        for (role, username, first_name, last_name, staff_id, dept_code, is_super) in STAFF_DATA:
            existing = User.objects.filter(username=username).first()
            if existing:
                self.stdout.write(f"  [EXISTS] Staff: {username} ({role})")
                continue

            dept_name = DEPT_NAMES.get(dept_code, 'Administration')
            user = User(
                username=username,
                email=f"{username}@ychst.edu.ng",
                first_name=first_name,
                last_name=last_name,
                role=role,
                must_change_password=False,
                is_staff=True,
                is_superuser=is_super,
                is_active=True,
            )
            user.set_password('Admin@1234')  # Staff default password
            user.save()

            StaffProfile.objects.get_or_create(
                user=user,
                defaults={
                    'staff_id': staff_id,
                    'department': dept_name,
                    'department_code': dept_code,
                    'current_rank': 'administrative',
                    'basic_salary': 0,
                }
            )

            self.stdout.write(
                self.style.SUCCESS(f"  [OK] {username} ({role})")
            )
            staff_created += 1

        # ── 3. Summary ─────────────────────────────────────────────────────
        self.stdout.write(self.style.MIGRATE_HEADING(f"\n{'='*60}"))
        self.stdout.write(self.style.SUCCESS(
            f"  [DONE]\n"
            f"     Students created : {total_created}\n"
            f"     Students existing: {total_existing}\n"
            f"     Staff created    : {staff_created}\n"
            f"\n  Default student password : {DEFAULT_PW}\n"
            f"  Default staff password   : Admin@1234\n"
            f"  All students must change password on first login.\n"
            f"{'='*60}"
        ))
