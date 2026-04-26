import os
import django
import sys
from django.utils import timezone

# Set up Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sanga_portal.settings')
django.setup()

from accounts.models import User, StudentProfile, StaffProfile

def seed_data():
    password = "12345678"
    
    # ─── DATA DEFINITIONS ────────────────────────────────────────────────────────
    
    student_data = {
        "PUBLIC HEALTH": [
            ("NUSAIBA MURTALA", "YCHST/2025/2026/PHT/001"),
            ("UGWU KINGSLEY CHINONSO", "YCHST/2025/2026/PHT/002"),
            ("LUCY ADAMU", "YCHST/2025/2026/PHT/003"),
            ("ABDULLAHI SHAMSUDEEN", "YCHST/2025/2026/PHT/004"),
            ("CHRRISTIANA HABILA", "YCHST/2025/2026/PHT/005"),
            ("JIBRIN AMINA", "YCHST/2025/2026/PHT/006"),
            ("UMAR FATIMA", "YCHST/2025/2026/PHT/007"),
            ("SULEIMAN HAJARA", "YCHST/2025/2026/PHT/008"),
            ("BILKISU MUSA", "YCHST/2025/2026/PHT/009"),
            ("MUKAILU FATIMA", "YCHST/2025/2026/PHT/010"),
            ("ZAKARI SHA’AWANATU", "YCHST/2025/2026/PHT/011"),
            ("SA’ADATU MUHAMMED", "YCHST/2025/2026/PHT/012"),
            ("ERNEST DANIEL", "YCHST/2025/2026/PHT/013"),
            ("BILKISU M. SALEH", "YCHST/2025/2026/PHT/014"),
            ("FAIZA IBRAHIM", "YCHST/2025/2026/PHT/015"),
            ("ADAMU AISHA ABANNI", "YCHST/2025/2026/PHT/016"),
            ("BENJAMIN NA’OMI", "YCHST/2025/2026/PHT/017"),
        ],
        "HEALTH INFORMATION": [
            ("ZUBAIRU AHMED MOHAMMED", "YCHST/2025/2026/HIMT/001"),
            ("DANLADI HAUWA", "YCHST/2025/2026/HIMT/002"),
            ("UBANDOMA LOIS", "YCHST/2025/2026/HIMT/003"),
            ("GOODNESS LUKA", "YCHST/2025/2026/HIMT/004"),
            ("SALIM ABDULLAHI", "YCHST/2025/2026/HIMT/005"),
            ("TANIMU DAUDA", "YCHST/2025/2026/HIMT/006"),
            ("ABUBAKAR KHALIFA YUSUF", "YCHST/2025/2026/HIMT/007"),
            ("PRECIOUS VIVIAN", "YCHST/2025/2026/HIMT/008"),
            ("HABIBA ABDULLAHI", "YCHST/2025/2026/HIMT/009"),
            ("KABIRU YAKUBU", "YCHST/2025/2026/HIMT/010"),
        ],
        "COMMUNITY HEALTH": [
            ("YUSUF JIBRRIN", "YCHST/2025/2026/CHEW/001"),
            ("ABDULLAHI MARYAM", "YCHST/2025/2026/CHEW/002"),
            ("USMAN MARYAM", "YCHST/2025/2026/CHEW/003"),
            ("ZUBAIDA IBRAHIM", "YCHST/2025/2026/CHEW/004"),
            ("FATIMA ABDULLAHI", "YCHST/2025/2026/CHEW/005"),
            ("HARIRA SULEIMAN YAMUSA", "YCHST/2025/2026/CHEW/006"),
            ("PAULINA BENJAMIN", "YCHST/2025/2026/CHEW/007"),
            ("FATIMA ALIYU ZAKARI", "YCHST/2025/2026/CHEW/008"),
            ("BLESSED ZAKKA", "YCHST/2025/2026/CHEW/009"),
            ("SOLOMON DESTINY", "YCHST/2025/2026/CHEW/010"),
            ("FATIMA ALIYU", "YCHST/2025/2026/CHEW/011"),
            ("SALAMATU IDRIS", "YCHST/2025/2026/CHEW/012"),
            ("SALISU BILKISU", "YCHST/2025/2026/CHEW/013"),
            ("UMMULKHAIRI JIBRIL", "YCHST/2025/2026/CHEW/014"),
            ("COMFORT NICOLAS", "YCHST/2025/2026/CHEW/015"),
            ("ABAMU BULUS", "YCHST/2025/2026/CHEW/016"),
            ("YUSIRA IBRAHIM", "YCHST/2025/2026/CHEW/017"),
            ("HAUWA ADAMU", "YCHST/2025/2026/CHEW/018"),
            ("FORBEARANCE PETER", "YCHST/2025/2026/CHEW/019"),
            ("BALA FAITH YAKUBU", "YCHST/2025/2026/CHEW/020"),
            ("KHADIJA ISIYA", "YCHST/2025/2026/CHEW/021"),
            ("SALOMI ISHAYA", "YCHST/2025/2026/CHEW/022"),
            ("ALHERI AMBI", "YCHST/2025/2026/CHEW/023"),
            ("MARKUS VALENTINA", "YCHST/2025/2026/CHEW/024"),
            ("HAJARA MOHAMMED", "YCHST/2025/2026/CHEW/025"),
            ("ABUBAKAR AISHA", "YCHST/2025/2026/CHEW/026"),
            ("BULUS MANZO", "YCHST/2025/2026/CHEW/027"),
            ("DORATHY JOEL", "YCHST/2025/2026/CHEW/028"),
            ("MATHIAS SAMUEL", "YCHST/2025/2026/CHEW/029"),
        ],
        "PHARMACY TECHNICIAN": [
            ("HAPPY NICHOLAS", "YCHST/2025/2026/PT/001"),
            ("GIMSON EZEKIEL", "YCHST/2025/2026/PT/002"),
            ("LAWAL MUHAMMADU SANI", "YCHST/2025/2026/PT/003"),
            ("ZULFA’U SALLAU BABALE", "YCHST/2025/2026/PT/004"),
            ("ABDULLAHI YUSUF AHMED", "YCHST/2025/2026/PT/005"),
            ("FATIMA MU’AZU", "YCHST/2025/2026/PT/006"),
            ("MUHIBBAT YUSUF", "YCHST/2025/2026/PT/007"),
            ("SALISU AMINU", "YCHST/2025/2026/PT/008"),
            ("KABIRU AHMED", "YCHST/2025/2026/PT/009"),
            ("HUSNAT MOHAMMED LAWAL", "YCHST/2025/2026/PT/010"),
            ("IDRIS NAFISAT ADAM", "YCHST/2025/2026/PT/011"),
            ("NANA KHADIJA ABDULLAHI", "YCHST/2025/2026/PT/012"),
            ("ELIJAH MATHEW", "YCHST/2025/2026/PT/013"),
            ("ISAAC BENJAMIN", "YCHST/2025/2026/PT/014"),
            ("MUSA MOHAMMED", "YCHST/2025/2026/PT/015"),
            ("FATIMA MOHAMMED", "YCHST/2025/2026/PT/016"),
            ("IDRIS ADAM", "YCHST/2025/2026/PT/017"),
            ("ASIYA DAUDA", "YCHST/2025/2026/PT/018"),
            ("MARYAM SHUAIBU", "YCHST/2025/2026/PT/019"),
            ("FAITH ADAMU JOSEPH", "YCHST/2025/2026/PT/020"),
            ("RILWAN ADAMU", "YCHST/2025/2026/PT/021"),
        ],
        "MEDICAL LABORATORY": [
            ("UMAR MUHAMMED", "YCHST/2025/2026/MLT/001"),
            ("MUSA BALARABE", "YCHST/2025/2026/MLT/002"),
            ("MARYAM KASIMU BABA", "YCHST/2025/2026/MLT/003"),
            ("SA’ADATU YA’U SULEIMAN", "YCHST/2025/2026/MLT/004"),
            ("BILYA AISHA MUSA", "YCHST/2025/2026/MLT/005"),
            ("HADIZA RABI’U", "YCHST/2025/2026/MLT/006"),
            ("KHADIJATU SANI", "YCHST/2025/2026/MLT/007"),
            ("RABECCA UBANDOMA", "YCHST/2025/2026/MLT/008"),
            ("GIMSON EZRA", "YCHST/2025/2026/MLT/009"),
            ("ADAMA IDRIS ISIYAKU", "YCHST/2025/2026/MLT/010"),
            ("ISRAEL BENJAMIN", "YCHST/2025/2026/MLT/011"),
            ("JOHN LOIS", "YCHST/2025/2026/MLT/012"),
            ("MUHAMMAD ANAS", "YCHST/2025/2026/MLT/013"),
            ("ALIYU UMMULKHAISI", "YCHST/2025/2026/MLT/014"),
            ("HAFSAT AKIBU", "YCHST/2025/2026/MLT/015"),
        ]
    }

    staff_roles = [
        (1, "Provost", "provost"),
        (2, "Registrar", "registrar"),
        (3, "Admin officer", "admin_officer"),
        (4, "Deputy Registrar", "deputy_registrar"),
        (5, "Bursar", "bursary"),
        (6, "Dean Students Affairs", "dean_students_affairs"),
        (7, "Academic Secretary", "academic_secretary"),
        (8, "Deputy Dean Students Affairs", "deputy_dean_students_affairs"),
        (9, "Practical Master", "practical_master"),
        (10, "Liaison Officer", "liaison_officer"),
    ]

    # ─── SEEDING STUDENTS ────────────────────────────────────────────────────────
    
    print("\n--- Seeding Students ---")
    for dept, students in student_data.items():
        print(f"Creating {dept} students...")
        for name, matric in students:
            # Simple name splitter
            name_parts = name.split()
            first_name = name_parts[0]
            last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else ""
            
            user, created = User.objects.update_or_create(
                username=matric,
                defaults={
                    'first_name': first_name,
                    'last_name': last_name,
                    'role': 'student',
                    'is_staff': False,
                    'is_active': True
                }
            )
            user.set_password(password)
            user.save()
            
            StudentProfile.objects.update_or_create(
                user=user,
                defaults={
                    'matriculation_number': matric,
                    'department': dept,
                    'faculty': 'Health Sciences',
                    'level': '100',
                    'program': dept.title(),
                    'admission_year': 2025,
                    'profile_completed': True
                }
            )
            print(f"  [OK] {matric} - {name}")

    # ─── SEEDING STAFF ───────────────────────────────────────────────────────────
    
    print("\n--- Seeding Staff ---")
    for level, rank_name, role_code in staff_roles:
        staff_id = f"YCHST/STF/{level:02d}/001"
        username = staff_id
        
        user, created = User.objects.update_or_create(
            username=username,
            defaults={
                'first_name': 'Principal',
                'last_name': rank_name,
                'role': role_code,
                'is_staff': True,
                'is_active': True
            }
        )
        user.set_password(password)
        user.save()
        
        StaffProfile.objects.update_or_create(
            user=user,
            defaults={
                'staff_id': staff_id,
                'department': 'Central Administration',
                'faculty': 'Administration',
                'current_rank': 'senior_lecturer' if level > 5 else 'professor',
                'date_of_first_appointment': timezone.now().date(),
                'date_of_current_appointment': timezone.now().date(),
                'basic_salary': 500000.00
            }
        )
        print(f"  [OK] {username} - {rank_name}")

    # Seeding 5 HODs and Coordinators
    for i in range(1, 6):
        depts = ["PH", "HIMT", "CHEW", "PT", "MLT"]
        dept = depts[i-1]
        
        # HOD
        hod_id = f"YCHST/HOD/{i:02d}/001"
        user, _ = User.objects.update_or_create(
            username=hod_id,
            defaults={'first_name': 'HOD', 'last_name': dept, 'role': 'hod', 'is_staff': True}
        )
        user.set_password(password)
        user.save()
        StaffProfile.objects.get_or_create(user=user, defaults={'staff_id': hod_id, 'department': dept, 'faculty': 'Health Sciences', 'date_of_first_appointment': timezone.now().date(), 'date_of_current_appointment': timezone.now().date(), 'basic_salary': 350000})
        print(f"  [OK] {hod_id} - HOD {dept}")
        
        # Coordinator
        coord_id = f"YCHST/COORD/{i:02d}/001"
        user, _ = User.objects.update_or_create(
            username=coord_id,
            defaults={'first_name': 'Coord', 'last_name': dept, 'role': 'hod_coordinator', 'is_staff': True}
        )
        user.set_password(password)
        user.save()
        StaffProfile.objects.get_or_create(user=user, defaults={'staff_id': coord_id, 'department': dept, 'faculty': 'Health Sciences', 'date_of_first_appointment': timezone.now().date(), 'date_of_current_appointment': timezone.now().date(), 'basic_salary': 300000})
        print(f"  [OK] {coord_id} - Coord {dept}")

    # Director
    dir_id = "YCHST/DIR/01/001"
    user, _ = User.objects.update_or_create(
        username=dir_id,
        defaults={'first_name': 'Institution', 'last_name': 'Director', 'role': 'director', 'is_staff': True, 'is_superuser': True}
    )
    user.set_password(password)
    user.save()
    StaffProfile.objects.get_or_create(user=user, defaults={'staff_id': dir_id, 'department': 'Owners Office', 'faculty': 'Administration', 'date_of_first_appointment': timezone.now().date(), 'date_of_current_appointment': timezone.now().date(), 'basic_salary': 1000000})
    print(f"  [OK] {dir_id} - Director (Owner)")

    print("\n--- Migration Summary ---")
    print(f"All usernames synchronized to Matric/Staff IDs.")
    print(f"All passwords set to: {password}")
    print("Cleanup complete!")

if __name__ == "__main__":
    seed_data()
