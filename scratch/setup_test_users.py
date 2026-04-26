import os
import django
import sys

# Set up Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sanga_portal.settings')
django.setup()

from accounts.models import User

def setup_test_users():
    password = "SangaTestPassword@2026"
    
    roles = [
        ('student', 'Student'),
        ('provost', 'Provost'),
        ('registrar', 'Registrar'),
        ('admin_officer', 'Administrative Officer'),
        ('deputy_registrar', 'Deputy Registrar'),
        ('bursary', 'Bursar'),
        ('dean_students_affairs', 'Dean of Student Affairs'),
        ('academic_secretary', 'Academic Secretary'),
        ('deputy_dean_students_affairs', 'Deputy Dean of Student Affairs'),
        ('practical_master', 'Practical Master'),
        ('liaison_officer', 'Liaison Officer'),
        ('hod', 'Head of Department'),
        ('director', 'Director'),
    ]

    print("--- Setting up Test Users ---")
    for role_code, role_name in roles:
        username = f"test_{role_code}"
        email = f"{role_code}@sanga.edu.ng"
        
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
                'first_name': 'Test',
                'last_name': role_name,
                'role': role_code,
                'is_staff': True if role_code != 'student' else False,
                'is_active': True
            }
        )
        
        user.set_password(password)
        user.role = role_code # Ensure role is correct if user already existed
        user.save()
        
        status = "Created" if created else "Updated"
        print(f"[{status}] Username: {username} | Role: {role_code}")

    print("\nSetup complete!")
    print(f"Default Password for all: {password}")

if __name__ == "__main__":
    setup_test_users()
