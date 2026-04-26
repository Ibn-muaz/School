import os
import django
import sys

# Set up Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sanga_portal.settings')
django.setup()

from courses.models import Course, CourseOffering

def seed_academic_data():
    academic_year = "2026/2027"
    
    # ── 1. Pharmacy Technician (PT) ──
    dept_pt = "Pharmacy Technician"
    pt_courses = [
        # Semester 1
        ("ENG 101", "USE OF ENGLISH", 2, "100", "first"),
        ("GNS 102", "CITIZENSHIP EDUCATION", 2, "100", "first"),
        ("ENT 101", "INTRODUCTION TO ENTREPRENEURSHIP", 1, "100", "first"),
        ("CSC 101", "INTRODUCTION TO COMPUTER SCIENCE", 2, "100", "first"),
        ("PHY 111", "GENERAL PHYSICS I", 2, "100", "first"),
        ("CHM 101", "GENERAL CHEMISTRY I", 3, "100", "first"),
        ("BIO 111", "GENERAL BIOLOGY I", 3, "100", "first"),
        ("MTH 111", "GENERAL MATHEMATICS I", 3, "100", "first"),
        ("BDT 151", "INTRODUCTION TO LABORATORY TECHNIQUES", 2, "100", "first"),
        ("PTP 111", "INTRODUCTION TO PRINCIPLE OF P.T.P", 2, "100", "first"),
        # Semester 2
        ("ENG 102", "COMMUNICATION SKILLS", 2, "100", "second"),
        ("PHY 112", "GENERAL PHYSICS II", 2, "100", "second"),
        ("CHM 112", "GENERAL CHEMISTRY II", 3, "100", "second"),
        ("BIO 112", "GENERAL BIOLOGY II", 3, "100", "second"),
        ("MTH 112", "GENERAL MATHEMATICS II", 2, "100", "second"),
        ("MCB 112", "BASIC MICROBIOLOGY I", 2, "100", "second"),
        ("BDT 152", "BASIC DISPENSING THEORY I", 3, "100", "second"),
        ("AUM 122", "INTRODUCTION TO ACTION & USES OF MEDICINE", 3, "100", "second"),
    ]

    # ── 2. General Health Sciences (Year 1) ──
    dept_ghs = "General Health Sciences"
    ghs_courses = [
        # Semester 1
        ("ELS 101", "Communication Skills I/Use of English I", 2, "100", "first"),
        # Use prefixes for common codes to avoid clashes if they belong to different syllabus
        ("GHS-CSC 101", "Introduction to IT I", 2, "100", "first"),
        ("GHS-CHM 101", "General Chemistry I", 3, "100", "first"),
        ("GHS-BIO 101", "General Biology I", 3, "100", "first"),
        ("GHS-PHY 101", "General Physics I", 3, "100", "first"),
        ("GHS-MTH 101", "General Mathematics I", 2, "100", "first"),
        ("GHS-GST 101", "Citizenship Education", 2, "100", "first"),
        ("GST 103", "History and Philosophy of Science", 2, "100", "first"),
        ("GHS-EHT 101", "Introduction to Environmental Health", 2, "100", "first"),
        ("FRN 101", "Functional French I", 2, "100", "first"),
        # Semester 2
        ("ELS 102", "Communication Skills II/Use of English II", 2, "100", "second"),
        ("GHS-CSC 102", "Introduction to IT II", 2, "100", "second"),
        ("GHS-PHY 102", "General Physics II", 3, "100", "second"),
        ("GHS-CHM 102", "Organic Chemistry", 3, "100", "second"),
        ("GHS-BIO 102", "General Biology II", 3, "100", "second"),
        ("GHS-MTH 102", "General Mathematics II", 2, "100", "second"),
        ("FAP 102", "First Aid and Primary Healthcare", 2, "100", "second"),
        ("GST 102", "Philosophy & Logic/ Critical Reasoning", 2, "100", "second"),
        ("FRN 102", "Functional French II", 2, "100", "second"),
    ]

    # ── 3. Community Health (CHEWS) ──
    dept_che = "Community Health"
    che_courses = [
        # Semester 1
        ("CHE 101", "Professional Ethics", 1, "100", "first"),
        ("CHE 103", "Anatomy and Physiology I", 2, "100", "first"),
        ("CHE 105", "Social Behaviour Change Communication", 2, "100", "first"),
        ("CHE 107", "Human Nutrition", 2, "100", "first"),
        ("CHE 109", "Introduction to Primary Health Care", 2, "100", "first"),
        ("GNS 101", "Use of English", 2, "100", "first"),
        ("GNS 103", "Citizenship Education", 1, "100", "first"),
        ("GNS 105", "Introduction to Medical Psychology", 1, "100", "first"),
        ("CHE 111", "Introduction to Medical Sociology", 2, "100", "first"),
        ("BCH 101", "Introduction to Physical Chemistry", 1, "100", "first"),
        ("CHE-EHT 101", "Introduction to Environmental Health", 2, "100", "first"),
        ("FOT 101", "Geography", 1, "100", "first"),
        ("COM 101", "Introduction to Computer", 2, "100", "first"),
        # Semester 2
        ("CHE 102", "Symptomatology", 2, "100", "second"),
        ("CHE 104", "Anatomy and Physiology II", 2, "100", "second"),
        ("CHE 106", "Reproductive Health", 2, "100", "second"),
        ("CHE 108", "Clinical Skills I", 3, "100", "second"),
        ("CHE 110", "Immunity and Immunization", 2, "100", "second"),
        ("CHE 112", "Control of Communicable Diseases", 2, "100", "second"),
        ("CHE 114", "Accident and Emergency", 2, "100", "second"),
        ("CHE 116", "Supervised Clinical Experience I", 3, "100", "second"),
        ("CHE 118", "Care and Management of HIV/AIDS", 1, "100", "second"),
        ("CHE-GNS 102", "Communication in English", 2, "100", "second"),
        ("STB 102", "Medical Laboratory Science Technology", 3, "100", "second"),
    ]

    # ── 4. ND Public Health Technology ──
    dept_pht = "ND Public Health Technology"
    pht_courses = [
        # Semester 1
        ("PHT 111", "Introduction to Public Health", 2, "100", "first"),
        ("PHT-MTH 101", "General Mathematics", 3, "100", "first"),
        ("STA 101", "Introduction to Statistics", 2, "100", "first"),
        ("GNS 230", "General Biology", 2, "100", "first"),
        ("PHT-GST 101", "Use of English", 2, "100", "first"),
        ("PHS 111", "Introduction to Pharmacology and Therapeutics", 2, "100", "first"),
        ("COM 111", "Introduction to Computer Science", 3, "100", "first"),
        ("PHT 112", "Immunology and Immunization", 2, "100", "first"),
        ("GLT 111", "General Laboratory Technique", 3, "100", "first"),
        ("DTH 115", "Introduction to Anatomy and Physiology", 3, "100", "first"),
        ("GNS 127", "Citizenship Education I", 2, "100", "first"),
    ]

    all_data = [
        (dept_pt, pt_courses),
        (dept_ghs, ghs_courses),
        (dept_che, che_courses),
        (dept_pht, pht_courses),
    ]

    total_courses = 0
    total_offerings = 0

    for dept, courses in all_data:
        print(f"Processing Department: {dept}...")
        for code, title, units, level, semester in courses:
            # Create or update Course
            course, created = Course.objects.update_or_create(
                course_code=code,
                defaults={
                    'course_title': title,
                    'credit_units': units,
                    'level': level,
                    'semester': semester,
                    'department': dept,
                    'faculty': dept,  # All levels are departmental
                    'is_active': True
                }
            )
            if created: total_courses += 1
            
            # Create CourseOffering
            offering, created_off = CourseOffering.objects.update_or_create(
                course=course,
                academic_year=academic_year,
                defaults={
                    'class_capacity': 100,
                    'is_active': True
                }
            )
            if created_off: total_offerings += 1

    print(f"\nSeeding complete!")
    print(f"New Courses: {total_courses}")
    print(f"New Offerings: {total_offerings} for {academic_year}")

if __name__ == "__main__":
    seed_academic_data()
