"""
Backfill StudentClearance records for existing students
who already have matric numbers.

Usage:
  python manage.py backfill_clearance
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings
from accounts.models import User
from clearance.models import StudentClearance, ClearanceStatusHistory


class Command(BaseCommand):
    help = 'Create StudentClearance records for existing students with matric numbers'

    def handle(self, *args, **options):
        students = User.objects.filter(role='student')
        created_count = 0
        skipped_count = 0
        academic_year = getattr(settings, 'CURRENT_ACADEMIC_YEAR', '2025/2026')

        for student in students:
            # Skip if clearance already exists
            if StudentClearance.objects.filter(student=student).exists():
                skipped_count += 1
                continue

            # Check if student has a matric number
            has_matric = False
            try:
                profile = student.student_profile
                has_matric = bool(profile.matriculation_number)
            except Exception:
                pass

            if has_matric:
                # Create fully approved clearance record
                clearance = StudentClearance.objects.create(
                    student=student,
                    academic_year=academic_year,
                    status='approved',
                    acceptance_fee_paid=True,
                    acceptance_fee_amount=25000.00,
                    acceptance_payment_ref='LEGACY-BACKFILL',
                    acceptance_paid_at=timezone.now(),
                    approved_at=timezone.now(),
                    matric_generated=True,
                    matric_generated_at=timezone.now(),
                    matric_locked=True,
                )

                ClearanceStatusHistory.objects.create(
                    clearance=clearance,
                    old_status='',
                    new_status='approved',
                    notes=f'Auto-created for existing student with matric: {profile.matriculation_number}',
                )
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'  [OK] {student.get_full_name()} - {profile.matriculation_number}'))
            else:
                # Create pending clearance record
                clearance = StudentClearance.objects.create(
                    student=student,
                    academic_year=academic_year,
                    status='pending_acceptance',
                )
                ClearanceStatusHistory.objects.create(
                    clearance=clearance,
                    old_status='',
                    new_status='pending_acceptance',
                    notes='Auto-created for existing student without matric.',
                )
                created_count += 1
                self.stdout.write(f'  [PENDING] {student.get_full_name()} - no matric (pending)')

        self.stdout.write(self.style.SUCCESS(
            f'\nDone! Created: {created_count} | Skipped (already exists): {skipped_count}'
        ))
