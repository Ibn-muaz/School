import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sanga_portal.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

from fees.models import FeeStructure

roles_to_create = [
    {'username': 'admin',         'password': 'SangaAdmin@2026',    'role': 'ict_director',   'first_name': 'ICT',      'last_name': 'Admin',     'email': 'ict@sanga.edu.ng'},
    {'username': 'student001',    'password': 'student1234',        'role': 'student',        'first_name': 'Emeka',    'last_name': 'Okonkwo',   'email': 'emeka@sanga.edu.ng'},
    {'username': 'lecturer001',   'password': 'SangaAdmin@2026',    'role': 'lecturer',       'first_name': 'Dr. Adaobi','last_name': 'Nwosu',    'email': 'adaobi@sanga.edu.ng'},
    {'username': 'hod001',        'password': 'SangaAdmin@2026',    'role': 'hod',            'first_name': 'Prof. Yemi','last_name': 'Adesanya',  'email': 'hod@sanga.edu.ng'},
    {'username': 'dean001',       'password': 'SangaAdmin@2026',    'role': 'dean_students_affairs', 'first_name': 'Prof. Bola','last_name': 'Adekunle',  'email': 'dean@sanga.edu.ng'},
    {'username': 'bursary001',    'password': 'SangaAdmin@2026',    'role': 'bursary',        'first_name': 'Ngozi',    'last_name': 'Eze',       'email': 'bursary@sanga.edu.ng'},
    {'username': 'registrar001',  'password': 'SangaAdmin@2026',    'role': 'registrar',      'first_name': 'Chidi',    'last_name': 'Okoro',     'email': 'registrar@sanga.edu.ng'},
    {'username': 'exams001',      'password': 'SangaAdmin@2026',    'role': 'exams_officer',  'first_name': 'Funke',    'last_name': 'Adeyemi',   'email': 'exams@sanga.edu.ng'},
    {'username': 'dir001',        'password': 'SangaAdmin@2026',    'role': 'director',       'first_name': 'Prof. Olu','last_name': 'Abiodun',   'email': 'director@sanga.edu.ng'},
    {'username': 'provost001',    'password': 'SangaAdmin@2026',    'role': 'provost',        'first_name': 'Prof. Isa', 'last_name': 'Garba',     'email': 'provost@sanga.edu.ng'},
    {'username': 'admin_off001',  'password': 'SangaAdmin@2026',    'role': 'admin_officer',  'first_name': 'Musa',     'last_name': 'Bello',     'email': 'admin@sanga.edu.ng'},
    {'username': 'hostel001',     'password': 'SangaAdmin@2026',    'role': 'hostel_admin',   'first_name': 'Zainab',   'last_name': 'Yusuf',     'email': 'hostel@sanga.edu.ng'},
    {'username': 'liaison001',    'password': 'SangaAdmin@2026',    'role': 'liaison_officer','first_name': 'Abubakar', 'last_name': 'Aliyu',     'email': 'liaison@sanga.edu.ng'},
]

staff_roles = {
    'lecturer', 'hod', 'dean_students_affairs', 'bursary', 'registrar', 'exams_officer', 
    'ict_director', 'director', 'provost', 'admin_officer', 'hostel_admin', 'liaison_officer'
}

created = 0
updated = 0
for data in roles_to_create:
    user, created_flag = User.objects.get_or_create(
        username=data['username'],
        defaults={
            'email': data['email'],
            'first_name': data['first_name'],
            'last_name': data['last_name'],
            'role': data['role'],
            'is_staff': data['role'] in staff_roles,
            'is_superuser': data['role'] == 'ict_director',
        },
    )

    if created_flag:
        user.set_password(data['password'])
        user.save()
        print(f"  Created: {user.username} ({data['role']})")
        created += 1
        continue

    changed = False
    for field in ('email', 'first_name', 'last_name', 'role'):
        if getattr(user, field) != data[field]:
            setattr(user, field, data[field])
            changed = True

    expected_staff = data['role'] in staff_roles
    if user.is_staff != expected_staff:
        user.is_staff = expected_staff
        changed = True

    expected_superuser = data['role'] == 'ict_director'
    if user.is_superuser != expected_superuser:
        user.is_superuser = expected_superuser
        changed = True
    
    # Always update password to match data
    user.set_password(data['password'])
    changed = True

    if changed:
        user.save()
        updated += 1
        print(f"  Updated: {user.username} ({data['role']})")
    else:
        print(f"  Exists: {user.username} ({data['role']})")

print(f"\nDone. {created} created, {updated} updated.")

from accounts.models import StudentProfile

# Create sample fee structure
print("\nCreating sample fee structure...")
fee_data = {
    'level': '100',
    'program': 'Medical Laboratory Science',
    'academic_year': '2024/2025',
    'tuition_fee_per_unit': 10000.00,  # ₦10,000 per credit unit
    'acceptance_fee': 25000.00,
    'registration_fee': 5000.00,
    'examination_fee': 15000.00,
    'library_fee': 5000.00,
    'medical_fee': 8000.00,
    'sports_fee': 3000.00,
    'development_fee': 10000.00,
    'hostel_fee': 45000.00,
    'other_fees': 2000.00,
    'is_active': True,
}

fee_structure, created = FeeStructure.objects.get_or_create(
    level=fee_data['level'],
    program=fee_data['program'],
    academic_year=fee_data['academic_year'],
    defaults=fee_data
)

if created:
    print(f"  Created fee structure: {fee_structure}")
else:
    # Update existing fee structure with new fields
    for key, value in fee_data.items():
        setattr(fee_structure, key, value)
    fee_structure.save()
    print(f"  Updated fee structure: {fee_structure}")

# Create student profile for student001
print("\nCreating student profile for student001...")
student_user = User.objects.get(username='student001')
profile_data = {
    'user': student_user,
    'matriculation_number': 'SNG/2024/001',
    'department': 'Medical Laboratory Science',
    'faculty': 'Basic Medical Sciences',
    'level': '100',
    'program': 'Medical Laboratory Science',
    'state_of_origin': 'Lagos',
    'local_government': 'Ikeja',
    'admission_year': 2024,
}

profile, created = StudentProfile.objects.get_or_create(
    user=student_user,
    defaults=profile_data
)

if created:
    print(f"  Created student profile: {profile}")
else:
    print(f"  Student profile already exists: {profile}")

print("\nAll done!")
