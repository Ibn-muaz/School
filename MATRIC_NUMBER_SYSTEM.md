"""
MATRICULATION NUMBER GENERATION SYSTEM
=======================================

This document describes how matriculation numbers are automatically generated
when students complete their admission and payment process.

FORMAT
------
YCHST/{ENTRY_YEAR}/{EXIT_YEAR}/{DEPARTMENT_CODE}/{SEQUENCE:03d}

Example: YCHST/2025/2026/PHT/001

DEPARTMENT CODES
----------------
- HIMT: Health Information Management Technology
- PHT:  Public Health Technology  
- CHEW: Community Health Extension Workers
- PT:   Pharmacy Technician
- MLT:  Medical Laboratory Technician

SEQUENCE NUMBERING
------------------
Each department maintains its own sequence counter starting from 001.
When a new student is admitted/pays fees:
- The system queries for the last matriculation number in that department
- Extracts the sequence number
- Increments and formats as 3-digit zero-padded number (001, 002, 003, etc.)

WORKFLOW
--------

1. STUDENT APPLIES
   - User registers as 'applicant'
   - ApplicationRecord created (status='started')

2. STUDENT PAYS FEE
   - FeePayment record created
   - Payment initiated via payment gateway
   - Payment verified → FeePayment.status = 'completed'

3. AUTOMATIC MATRIC GENERATION (Payment Verification)
   - When verify_payment() is called:
     a. Checks if StudentProfile exists
     b. If not, creates StudentProfile with matriculation number
     c. Extracts department from ApplicationRecord
     d. Calls generate_matriculation_number()
     e. Saves generated matric to database

4. REGISTRAR ADMISSION DECISION (Optional)
   - Registrar reviews application
   - Decides to admit or reject
   - If admit → ApplicationRecord.status = 'admitted'
                 User.role changed to 'student'
                 StudentProfile created (if not already by payment)
                 Matriculation number assigned (if not already)

FILES INVOLVED
--------------

accounts/matric_utils.py:
  - generate_matriculation_number(department, academic_year)
  - get_department_code(department)
  - get_next_sequence_number(dept_code, academic_year)
  - validate_matriculation_uniqueness(matric_number)

admissions/registrar_views.py (process_admission_decision):
  - Imports: generate_matriculation_number, get_department_code
  - Creates StudentProfile with matric after admission decision

fees/views.py (verify_payment):
  - Imports: generate_matriculation_number, StudentProfile
  - Creates StudentProfile with matric after payment verification

USAGE EXAMPLES
--------------

# Generate matric for a new student
from accounts.matric_utils import generate_matriculation_number

matric = generate_matriculation_number(
    department='Public Health Technology (PHT)',
    academic_year='2025/2026'
)
# Returns: YCHST/2025/2026/PHT/018 (if 17 students already exist for PHT)

# Get department code
from accounts.matric_utils import get_department_code

code = get_department_code('Health Information Management Technology (HIMT)')
# Returns: HIMT

# Check uniqueness
from accounts.matric_utils import validate_matriculation_uniqueness

is_unique = validate_matriculation_uniqueness('YCHST/2025/2026/PHT/050')
# Returns: True (if matric doesn't exist), False (if it does)

EXISTING STUDENTS DATA
----------------------

Current enrollment by department (as of 2025/2026):
- PHT (Public Health Technology): 17 students (001-017)
- HIMT (Health Information): 10 students (001-010)
- CHEW (Community Health): 29 students (001-029)
- PT (Pharmacy Technician): 21 students (001-021)
- MLT (Medical Laboratory): 15 students (001-015)

New students in each department will continue from:
- PHT: 018
- HIMT: 011
- CHEW: 030
- PT: 022
- MLT: 016

IMPORTANT NOTES
---------------

1. The academic_year parameter in generate_matriculation_number() should be
   updated yearly (e.g., 2025/2026 → 2026/2027)

2. The system supports flexible department name matching:
   - Full names: 'Public Health Technology (PHT)'
   - Short codes: 'PHT', 'pht'
   - Partial matches: 'Public Health', 'public_health'

3. If a student's department cannot be determined, matric generation will fail
   gracefully with a ValueError that's caught and logged.

4. The system handles the case where StudentProfile doesn't exist yet:
   - payment verification creates it
   - admission decision also creates/updates it
   
5. Matriculation numbers are UNIQUE in the database:
   - Enforced by StudentProfile.matriculation_number unique=True

TESTING
-------

Run the test script:
  python test_matric.py

This tests:
- Department code mapping
- Sequence number calculation
- Full matric generation
- Uniqueness validation
"""
