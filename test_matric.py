#!/usr/bin/env python
"""
Test script for matriculation number generation
Run: python manage.py shell < test_matric.py
Or: python test_matric.py (if in Django environment)
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sanga_portal.settings')
django.setup()

from accounts.matric_utils import (
    generate_matriculation_number,
    get_department_code,
    get_next_sequence_number,
    validate_matriculation_uniqueness,
    DEPARTMENT_CODES
)

print("=" * 80)
print("MATRICULATION NUMBER GENERATION TEST")
print("=" * 80)

# Test 1: Department code mapping
print("\n1. Testing Department Code Mapping:")
test_departments = [
    'Public Health Technology (PHT)',
    'Health Information Management Technology (HIMT)',
    'Community Health Extension Workers (CHEW)',
    'Pharmacy Technician (PT)',
    'Medical Laboratory Technician (MLT)',
]

for dept in test_departments:
    try:
        code = get_department_code(dept)
        print(f"   ✓ {dept:<50} → {code}")
    except ValueError as e:
        print(f"   ✗ {dept:<50} → ERROR: {e}")

# Test invalid department
print("\n   Testing invalid department:")
try:
    code = get_department_code('Invalid Department')
    print(f"   ✗ Should have raised ValueError but got: {code}")
except ValueError as e:
    print(f"   ✓ Correctly raised ValueError: {e}")

# Test 2: Next sequence number calculation
print("\n2. Testing Next Sequence Number Calculation:")
for dept_code in ['PHT', 'HIMT', 'CHEW', 'PT', 'MLT']:
    next_seq = get_next_sequence_number(dept_code)
    print(f"   {dept_code}: Next sequence number = {next_seq:03d}")

# Test 3: Generate full matriculation numbers
print("\n3. Testing Full Matriculation Number Generation:")
for dept in test_departments:
    try:
        matric = generate_matriculation_number(dept)
        print(f"   ✓ {dept:<50} → {matric}")
    except Exception as e:
        print(f"   ✗ {dept:<50} → ERROR: {e}")

# Test 4: Test uniqueness validation
print("\n4. Testing Matriculation Uniqueness Validation:")
from accounts.models import StudentProfile

# Create a test matric if possible
test_matric = "YCHST/2025/2026/PHT/999"
is_unique = validate_matriculation_uniqueness(test_matric)
print(f"   '{test_matric}' is unique: {is_unique}")

print("\n" + "=" * 80)
print("TESTS COMPLETE")
print("=" * 80)
