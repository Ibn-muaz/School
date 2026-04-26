"""
Management command: seed_courses
Seeds the full curriculum course list for all programmes at Yar'yaya College.
Run with: python manage.py seed_courses
"""
from django.core.management.base import BaseCommand
from courses.models import Course


COURSES = [
    # ────────────────────────────────────────────────────────────────
    # PROGRAMME: Pharmacy Technology (BDT/PTP)
    # ────────────────────────────────────────────────────────────────
    # 100 Level — First Semester
    {'code': 'ENG 101', 'title': 'Use of English',                          'units': 2, 'level': '100', 'sem': 'first',  'dept': 'Pharmacy Technology', 'fac': 'Health Sciences'},
    {'code': 'GNS 102', 'title': 'Citizenship Education',                   'units': 2, 'level': '100', 'sem': 'first',  'dept': 'Pharmacy Technology', 'fac': 'Health Sciences'},
    {'code': 'ENT 101', 'title': 'Introduction to Entrepreneurship',         'units': 1, 'level': '100', 'sem': 'first',  'dept': 'Pharmacy Technology', 'fac': 'Health Sciences'},
    {'code': 'CSC 101', 'title': 'Introduction to Computer Science',         'units': 2, 'level': '100', 'sem': 'first',  'dept': 'Pharmacy Technology', 'fac': 'Health Sciences'},
    {'code': 'PHY 111', 'title': 'General Physics I',                        'units': 2, 'level': '100', 'sem': 'first',  'dept': 'Pharmacy Technology', 'fac': 'Health Sciences'},
    {'code': 'CHM 101', 'title': 'General Chemistry I',                      'units': 3, 'level': '100', 'sem': 'first',  'dept': 'Pharmacy Technology', 'fac': 'Health Sciences'},
    {'code': 'BIO 111', 'title': 'General Biology I',                        'units': 3, 'level': '100', 'sem': 'first',  'dept': 'Pharmacy Technology', 'fac': 'Health Sciences'},
    {'code': 'MTH 111', 'title': 'General Mathematics I',                    'units': 3, 'level': '100', 'sem': 'first',  'dept': 'Pharmacy Technology', 'fac': 'Health Sciences'},
    {'code': 'BDT 151', 'title': 'Introduction to Laboratory Techniques',    'units': 2, 'level': '100', 'sem': 'first',  'dept': 'Pharmacy Technology', 'fac': 'Health Sciences'},
    {'code': 'PTP 111', 'title': 'Introduction to Principle of P.T.P',       'units': 2, 'level': '100', 'sem': 'first',  'dept': 'Pharmacy Technology', 'fac': 'Health Sciences'},

    # 100 Level — Second Semester
    {'code': 'ENG 102', 'title': 'Communication Skills',                     'units': 2, 'level': '100', 'sem': 'second', 'dept': 'Pharmacy Technology', 'fac': 'Health Sciences'},
    {'code': 'PHY 112', 'title': 'General Physics II',                       'units': 2, 'level': '100', 'sem': 'second', 'dept': 'Pharmacy Technology', 'fac': 'Health Sciences'},
    {'code': 'CHM 102', 'title': 'General Chemistry II',                     'units': 3, 'level': '100', 'sem': 'second', 'dept': 'Pharmacy Technology', 'fac': 'Health Sciences'},
    {'code': 'BIO 112', 'title': 'General Biology II',                       'units': 3, 'level': '100', 'sem': 'second', 'dept': 'Pharmacy Technology', 'fac': 'Health Sciences'},
    {'code': 'MTH 112', 'title': 'General Mathematics II',                   'units': 2, 'level': '100', 'sem': 'second', 'dept': 'Pharmacy Technology', 'fac': 'Health Sciences'},
    {'code': 'MCB 112', 'title': 'Basic Microbiology I',                     'units': 2, 'level': '100', 'sem': 'second', 'dept': 'Pharmacy Technology', 'fac': 'Health Sciences'},
    {'code': 'BDT 152', 'title': 'Basic Dispensing Theory I',                'units': 3, 'level': '100', 'sem': 'second', 'dept': 'Pharmacy Technology', 'fac': 'Health Sciences'},
    {'code': 'AUM 122', 'title': 'Introduction to Action & Uses of Medicine','units': 3, 'level': '100', 'sem': 'second', 'dept': 'Pharmacy Technology', 'fac': 'Health Sciences'},

    # ────────────────────────────────────────────────────────────────
    # PROGRAMME: Environmental Health Technology (EHT)
    # ────────────────────────────────────────────────────────────────
    # Year 1 (100 Level) — First Semester
    {'code': 'ELS 101', 'title': 'Communication Skills I / Use of English I',     'units': 2, 'level': '100', 'sem': 'first',  'dept': 'Environmental Health Technology', 'fac': 'Health Sciences'},
    {'code': 'CSC 101B','title': 'Introduction to IT I',                           'units': 2, 'level': '100', 'sem': 'first',  'dept': 'Environmental Health Technology', 'fac': 'Health Sciences'},
    {'code': 'CHM 101B','title': 'General Chemistry I',                            'units': 3, 'level': '100', 'sem': 'first',  'dept': 'Environmental Health Technology', 'fac': 'Health Sciences'},
    {'code': 'BIO 101', 'title': 'General Biology I',                              'units': 3, 'level': '100', 'sem': 'first',  'dept': 'Environmental Health Technology', 'fac': 'Health Sciences'},
    {'code': 'PHY 101', 'title': 'General Physics I',                              'units': 3, 'level': '100', 'sem': 'first',  'dept': 'Environmental Health Technology', 'fac': 'Health Sciences'},
    {'code': 'MTH 101', 'title': 'General Mathematics I',                          'units': 2, 'level': '100', 'sem': 'first',  'dept': 'Environmental Health Technology', 'fac': 'Health Sciences'},
    {'code': 'GST 101', 'title': 'Citizenship Education',                          'units': 2, 'level': '100', 'sem': 'first',  'dept': 'Environmental Health Technology', 'fac': 'Health Sciences'},
    {'code': 'GST 103', 'title': 'History and Philosophy of Science',              'units': 2, 'level': '100', 'sem': 'first',  'dept': 'Environmental Health Technology', 'fac': 'Health Sciences'},
    {'code': 'EHT 101', 'title': 'Introduction to Environmental Health',           'units': 2, 'level': '100', 'sem': 'first',  'dept': 'Environmental Health Technology', 'fac': 'Health Sciences'},
    {'code': 'FRN 101', 'title': 'Functional French I',                            'units': 2, 'level': '100', 'sem': 'first',  'dept': 'Environmental Health Technology', 'fac': 'Health Sciences'},

    # Year 1 (100 Level) — Second Semester
    {'code': 'ELS 102', 'title': 'Communication Skills II / Use of English II',    'units': 2, 'level': '100', 'sem': 'second', 'dept': 'Environmental Health Technology', 'fac': 'Health Sciences'},
    {'code': 'CSC 102', 'title': 'Introduction to IT II',                          'units': 2, 'level': '100', 'sem': 'second', 'dept': 'Environmental Health Technology', 'fac': 'Health Sciences'},
    {'code': 'PHY 102', 'title': 'General Physics II',                             'units': 3, 'level': '100', 'sem': 'second', 'dept': 'Environmental Health Technology', 'fac': 'Health Sciences'},
    {'code': 'CHM 102B','title': 'Organic Chemistry',                              'units': 3, 'level': '100', 'sem': 'second', 'dept': 'Environmental Health Technology', 'fac': 'Health Sciences'},
    {'code': 'BIO 102', 'title': 'General Biology II',                             'units': 3, 'level': '100', 'sem': 'second', 'dept': 'Environmental Health Technology', 'fac': 'Health Sciences'},
    {'code': 'MTH 102', 'title': 'General Mathematics II',                         'units': 2, 'level': '100', 'sem': 'second', 'dept': 'Environmental Health Technology', 'fac': 'Health Sciences'},
    {'code': 'FAP 102', 'title': 'First Aid and Primary Healthcare',               'units': 2, 'level': '100', 'sem': 'second', 'dept': 'Environmental Health Technology', 'fac': 'Health Sciences'},
    {'code': 'GST 102', 'title': 'Philosophy & Logic / Critical Reasoning',        'units': 2, 'level': '100', 'sem': 'second', 'dept': 'Environmental Health Technology', 'fac': 'Health Sciences'},
    {'code': 'FRN 102', 'title': 'Functional French II',                           'units': 2, 'level': '100', 'sem': 'second', 'dept': 'Environmental Health Technology', 'fac': 'Health Sciences'},

    # ────────────────────────────────────────────────────────────────
    # PROGRAMME: Community Health (CHEW Diploma)
    # ────────────────────────────────────────────────────────────────
    # Year 1 — First Semester
    {'code': 'CHE 101', 'title': 'Professional Ethics',                          'units': 1, 'level': '100', 'sem': 'first',  'dept': 'Community Health (CHEW)', 'fac': 'Health Sciences'},
    {'code': 'CHE 103', 'title': 'Anatomy and Physiology I',                     'units': 2, 'level': '100', 'sem': 'first',  'dept': 'Community Health (CHEW)', 'fac': 'Health Sciences'},
    {'code': 'CHE 105', 'title': 'Social Behaviour Change Communication',        'units': 2, 'level': '100', 'sem': 'first',  'dept': 'Community Health (CHEW)', 'fac': 'Health Sciences'},
    {'code': 'CHE 107A','title': 'Human Nutrition',                              'units': 2, 'level': '100', 'sem': 'first',  'dept': 'Community Health (CHEW)', 'fac': 'Health Sciences'},
    {'code': 'CHE 109', 'title': 'Introduction to Primary Health Care',          'units': 2, 'level': '100', 'sem': 'first',  'dept': 'Community Health (CHEW)', 'fac': 'Health Sciences'},
    {'code': 'GNS 101', 'title': 'Use of English',                               'units': 2, 'level': '100', 'sem': 'first',  'dept': 'Community Health (CHEW)', 'fac': 'Health Sciences'},
    {'code': 'GNS 103', 'title': 'Citizenship Education',                        'units': 1, 'level': '100', 'sem': 'first',  'dept': 'Community Health (CHEW)', 'fac': 'Health Sciences'},
    {'code': 'GNS 105', 'title': 'Introduction to Medical Psychology',           'units': 1, 'level': '100', 'sem': 'first',  'dept': 'Community Health (CHEW)', 'fac': 'Health Sciences'},
    {'code': 'CHE 107B','title': 'Introduction to Medical Sociology',            'units': 2, 'level': '100', 'sem': 'first',  'dept': 'Community Health (CHEW)', 'fac': 'Health Sciences'},
    {'code': 'BCH 101', 'title': 'Introduction to Physical Chemistry',           'units': 1, 'level': '100', 'sem': 'first',  'dept': 'Community Health (CHEW)', 'fac': 'Health Sciences'},
    {'code': 'EHT 101B','title': 'Introduction to Environmental Health',         'units': 2, 'level': '100', 'sem': 'first',  'dept': 'Community Health (CHEW)', 'fac': 'Health Sciences'},
    {'code': 'FOT 101', 'title': 'Geography',                                    'units': 1, 'level': '100', 'sem': 'first',  'dept': 'Community Health (CHEW)', 'fac': 'Health Sciences'},
    {'code': 'COM 101', 'title': 'Introduction to Computer',                     'units': 2, 'level': '100', 'sem': 'first',  'dept': 'Community Health (CHEW)', 'fac': 'Health Sciences'},

    # Year 1 — Second Semester
    {'code': 'CHE 102', 'title': 'Symptomatology',                              'units': 2, 'level': '100', 'sem': 'second', 'dept': 'Community Health (CHEW)', 'fac': 'Health Sciences'},
    {'code': 'CHE 104', 'title': 'Anatomy and Physiology II',                   'units': 2, 'level': '100', 'sem': 'second', 'dept': 'Community Health (CHEW)', 'fac': 'Health Sciences'},
    {'code': 'CHE 106', 'title': 'Reproductive Health',                         'units': 2, 'level': '100', 'sem': 'second', 'dept': 'Community Health (CHEW)', 'fac': 'Health Sciences'},
    {'code': 'CHE 108', 'title': 'Clinical Skills I',                           'units': 3, 'level': '100', 'sem': 'second', 'dept': 'Community Health (CHEW)', 'fac': 'Health Sciences'},
    {'code': 'CHE 110', 'title': 'Immunity and Immunization',                   'units': 2, 'level': '100', 'sem': 'second', 'dept': 'Community Health (CHEW)', 'fac': 'Health Sciences'},
    {'code': 'CHE 112', 'title': 'Control of Communicable Diseases',            'units': 2, 'level': '100', 'sem': 'second', 'dept': 'Community Health (CHEW)', 'fac': 'Health Sciences'},
    {'code': 'CHE 114', 'title': 'Accident and Emergency',                      'units': 2, 'level': '100', 'sem': 'second', 'dept': 'Community Health (CHEW)', 'fac': 'Health Sciences'},
    {'code': 'CHE 116', 'title': 'Supervised Clinical Experience I',            'units': 3, 'level': '100', 'sem': 'second', 'dept': 'Community Health (CHEW)', 'fac': 'Health Sciences'},
    {'code': 'CHE 118', 'title': 'Care and Management of HIV/AIDS',             'units': 1, 'level': '100', 'sem': 'second', 'dept': 'Community Health (CHEW)', 'fac': 'Health Sciences'},
    {'code': 'GNS 102', 'title': 'Communication in English',                    'units': 2, 'level': '100', 'sem': 'second', 'dept': 'Community Health (CHEW)', 'fac': 'Health Sciences'},
    {'code': 'STB 102', 'title': 'Medical Laboratory Science Technology',       'units': 3, 'level': '100', 'sem': 'second', 'dept': 'Community Health (CHEW)', 'fac': 'Health Sciences'},

    # ────────────────────────────────────────────────────────────────
    # PROGRAMME: ND Public Health Technology (PHT)
    # ────────────────────────────────────────────────────────────────
    # 100 Level — First Semester
    {'code': 'PHT 111', 'title': 'Introduction to Public Health',                       'units': 2, 'level': '100', 'sem': 'first', 'dept': 'Public Health Technology', 'fac': 'Health Sciences'},
    {'code': 'MTH 101B','title': 'General Mathematics',                                 'units': 3, 'level': '100', 'sem': 'first', 'dept': 'Public Health Technology', 'fac': 'Health Sciences'},
    {'code': 'STA 101', 'title': 'Introduction to Statistics',                          'units': 2, 'level': '100', 'sem': 'first', 'dept': 'Public Health Technology', 'fac': 'Health Sciences'},
    {'code': 'GNS 230', 'title': 'General Biology',                                     'units': 2, 'level': '100', 'sem': 'first', 'dept': 'Public Health Technology', 'fac': 'Health Sciences'},
    {'code': 'GST 101B','title': 'Use of English',                                      'units': 2, 'level': '100', 'sem': 'first', 'dept': 'Public Health Technology', 'fac': 'Health Sciences'},
    {'code': 'PHS 111', 'title': 'Introduction to Pharmacology and Therapeutics',       'units': 2, 'level': '100', 'sem': 'first', 'dept': 'Public Health Technology', 'fac': 'Health Sciences'},
    {'code': 'COM 111', 'title': 'Introduction to Computer Science',                    'units': 3, 'level': '100', 'sem': 'first', 'dept': 'Public Health Technology', 'fac': 'Health Sciences'},
    {'code': 'PHT 112', 'title': 'Immunology and Immunization',                         'units': 2, 'level': '100', 'sem': 'first', 'dept': 'Public Health Technology', 'fac': 'Health Sciences'},
    {'code': 'GLT 111', 'title': 'General Laboratory Technique',                        'units': 3, 'level': '100', 'sem': 'first', 'dept': 'Public Health Technology', 'fac': 'Health Sciences'},
    {'code': 'DTH 115', 'title': 'Introduction to Anatomy and Physiology',              'units': 3, 'level': '100', 'sem': 'first', 'dept': 'Public Health Technology', 'fac': 'Health Sciences'},
    {'code': 'GNS 127', 'title': 'Citizenship Education I',                             'units': 2, 'level': '100', 'sem': 'first', 'dept': 'Public Health Technology', 'fac': 'Health Sciences'},
]


class Command(BaseCommand):
    help = 'Seeds all curriculum courses for Yar\'yaya College programmes'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear', action='store_true',
            help='Clear existing courses before seeding (use with caution)'
        )

    def handle(self, *args, **options):
        if options['clear']:
            deleted, _ = Course.objects.all().delete()
            self.stdout.write(self.style.WARNING(f'Cleared {deleted} existing courses.'))

        created_count = 0
        updated_count = 0

        for c in COURSES:
            obj, created = Course.objects.update_or_create(
                course_code=c['code'],
                defaults={
                    'course_title': c['title'],
                    'credit_units': c['units'],
                    'level':        c['level'],
                    'semester':     c['sem'],
                    'department':   c['dept'],
                    'faculty':      c['fac'],
                    'is_active':    True,
                }
            )
            if created:
                created_count += 1
                self.stdout.write(f'  + Created: {c["code"]} — {c["title"]}')
            else:
                updated_count += 1

        self.stdout.write(self.style.SUCCESS(
            f'\nDone. {created_count} courses created, {updated_count} updated.'
        ))
        self.stdout.write(self.style.NOTICE(
            'Programmes seeded:\n'
            '  - Pharmacy Technology\n'
            '  - Environmental Health Technology\n'
            '  - Community Health (CHEW Diploma)\n'
            '  - ND Public Health Technology\n'
        ))
