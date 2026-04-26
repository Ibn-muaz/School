"""
Management command: seed_fees
Seeds fee structures for all 5 departments at YCHST Sanga for 2025/2026 session.

Usage:
    python manage.py seed_fees
    python manage.py seed_fees --clear   (wipe first, then reseed)
    python manage.py seed_fees --year 2026/2027

Nigerian polytechnic/college fee structure (amounts in Naira).
All levels get the same core fees; 200-level students pay a reduced acceptance fee.
"""

from django.core.management.base import BaseCommand


# ─── Fee Structures per Department/Level ─────────────────────────────────────
# Amounts in Naira (NGN). Adjust as needed.
# Format: (dept_code, dept_name, level, tuition/unit, acceptance, reg, exam, library, medical, sports, development, other)

FEE_SCHEDULE = {
    # Public Health Technology — 4.0 scale
    'PHT': {
        'name': 'Public Health Technology',
        'levels': {
            '100': {
                'acceptance_fee':   25000,
                'registration_fee': 15000,
                'examination_fee':  10000,
                'library_fee':       3000,
                'medical_fee':       5000,
                'sports_fee':        2000,
                'development_fee':  10000,
                'hostel_fee':            0,
                'other_fees':        5000,
            },
            '200': {
                'acceptance_fee':       0,   # No acceptance fee from 200 level
                'registration_fee': 15000,
                'examination_fee':  10000,
                'library_fee':       3000,
                'medical_fee':       5000,
                'sports_fee':        2000,
                'development_fee':  10000,
                'hostel_fee':            0,
                'other_fees':        5000,
            },
        }
    },

    # Health Information Management Technology — 5.0 scale (HIMT)
    'HIMT': {
        'name': 'Health Information Management Technology',
        'levels': {
            '100': {
                'acceptance_fee':   25000,
                'registration_fee': 15000,
                'examination_fee':  10000,
                'library_fee':       3000,
                'medical_fee':       5000,
                'sports_fee':        2000,
                'development_fee':  12000,
                'hostel_fee':            0,
                'other_fees':        5000,
            },
            '200': {
                'acceptance_fee':       0,
                'registration_fee': 15000,
                'examination_fee':  10000,
                'library_fee':       3000,
                'medical_fee':       5000,
                'sports_fee':        2000,
                'development_fee':  12000,
                'hostel_fee':            0,
                'other_fees':        5000,
            },
        }
    },

    # Community Health Extension Workers (CHEW)
    'CHEW': {
        'name': 'Community Health Extension Workers',
        'levels': {
            '100': {
                'acceptance_fee':   20000,
                'registration_fee': 12000,
                'examination_fee':   8000,
                'library_fee':       2500,
                'medical_fee':       4000,
                'sports_fee':        1500,
                'development_fee':   8000,
                'hostel_fee':            0,
                'other_fees':        4000,
            },
            '200': {
                'acceptance_fee':       0,
                'registration_fee': 12000,
                'examination_fee':   8000,
                'library_fee':       2500,
                'medical_fee':       4000,
                'sports_fee':        1500,
                'development_fee':   8000,
                'hostel_fee':            0,
                'other_fees':        4000,
            },
        }
    },

    # Pharmacy Technician (PT)
    'PT': {
        'name': 'Pharmacy Technician',
        'levels': {
            '100': {
                'acceptance_fee':   25000,
                'registration_fee': 15000,
                'examination_fee':  10000,
                'library_fee':       3000,
                'medical_fee':       5000,
                'sports_fee':        2000,
                'development_fee':  10000,
                'hostel_fee':            0,
                'other_fees':        5000,
            },
            '200': {
                'acceptance_fee':       0,
                'registration_fee': 15000,
                'examination_fee':  10000,
                'library_fee':       3000,
                'medical_fee':       5000,
                'sports_fee':        2000,
                'development_fee':  10000,
                'hostel_fee':            0,
                'other_fees':        5000,
            },
        }
    },

    # Medical Laboratory Technician (MLT)
    'MLT': {
        'name': 'Medical Laboratory Technician',
        'levels': {
            '100': {
                'acceptance_fee':   25000,
                'registration_fee': 15000,
                'examination_fee':  12000,
                'library_fee':       3000,
                'medical_fee':       5000,
                'sports_fee':        2000,
                'development_fee':  12000,
                'hostel_fee':            0,
                'other_fees':        6000,
            },
            '200': {
                'acceptance_fee':       0,
                'registration_fee': 15000,
                'examination_fee':  12000,
                'library_fee':       3000,
                'medical_fee':       5000,
                'sports_fee':        2000,
                'development_fee':  12000,
                'hostel_fee':            0,
                'other_fees':        6000,
            },
        }
    },
}


class Command(BaseCommand):
    help = "Seed fee structures for all 5 YCHST departments (2025/2026 session)"

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Delete all existing FeeStructure records before seeding',
        )
        parser.add_argument(
            '--year',
            type=str,
            default='2025/2026',
            help='Academic year to seed (default: 2025/2026)',
        )

    def handle(self, *args, **options):
        from fees.models import FeeStructure

        academic_year = options['year']

        if options['clear']:
            deleted, _ = FeeStructure.objects.filter(academic_year=academic_year).delete()
            self.stdout.write(self.style.WARNING(
                f"Cleared {deleted} FeeStructure records for {academic_year}."
            ))

        self.stdout.write(self.style.MIGRATE_HEADING(
            f"\n{'='*60}\n  YCHST Fee Structure Seeder — {academic_year}\n{'='*60}"
        ))

        created_count = 0
        updated_count = 0

        for dept_code, dept_data in FEE_SCHEDULE.items():
            dept_name = dept_data['name']
            self.stdout.write(f"\n  [{dept_code}] {dept_name}")

            for level, fees in dept_data['levels'].items():
                # Use 'program' field as dept_code so the bursary can filter by dept
                obj, created = FeeStructure.objects.update_or_create(
                    level=level,
                    program=dept_code,
                    academic_year=academic_year,
                    defaults={
                        'acceptance_fee':   fees['acceptance_fee'],
                        'registration_fee': fees['registration_fee'],
                        'examination_fee':  fees['examination_fee'],
                        'library_fee':      fees['library_fee'],
                        'medical_fee':      fees['medical_fee'],
                        'sports_fee':       fees['sports_fee'],
                        'development_fee':  fees['development_fee'],
                        'hostel_fee':       fees['hostel_fee'],
                        'other_fees':       fees['other_fees'],
                        'tuition_fee_per_unit': 0,
                        'is_active': True,
                    }
                )

                total = obj.total_fee
                status = "[NEW]" if created else "[UPDATED]"
                self.stdout.write(
                    self.style.SUCCESS(
                        f"    {status} Level {level} — Total: N{total:,.0f}"
                    )
                )
                if created:
                    created_count += 1
                else:
                    updated_count += 1

        self.stdout.write(self.style.MIGRATE_HEADING(f"\n{'='*60}"))
        self.stdout.write(self.style.SUCCESS(
            f"  [DONE]\n"
            f"     Fee structures created : {created_count}\n"
            f"     Fee structures updated : {updated_count}\n"
            f"     Academic year          : {academic_year}\n"
            f"     Departments            : PHT, HIMT, CHEW, PT, MLT\n"
            f"     Levels                 : 100, 200\n"
            f"{'='*60}"
        ))
