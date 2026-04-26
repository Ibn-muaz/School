"""
Matriculation number generation utilities.

Format: YCHST/{ENTRY_YEAR}/{EXIT_YEAR}/{DEPT_CODE}/{SEQUENCE:03d}
Example: YCHST/2025/2026/PHT/001
"""

from django.db.models import Max, Q
from accounts.models import StudentProfile


# Department code mapping based on program/department
DEPARTMENT_CODES = {
    'Health Information Management Technology (HIMT)': 'HIMT',
    'HIMT': 'HIMT',
    'health_information': 'HIMT',
    'himt': 'HIMT',
    
    'Public Health Technology (PHT)': 'PHT',
    'PHT': 'PHT',
    'public_health': 'PHT',
    'pht': 'PHT',
    
    'Community Health Extension Workers (CHEW)': 'CHEW',
    'CHEW': 'CHEW',
    'community_health': 'CHEW',
    'chew': 'CHEW',
    
    'Pharmacy Technician (PT)': 'PT',
    'PT': 'PT',
    'pharmacy_technician': 'PT',
    'pt': 'PT',
    
    'Medical Laboratory Technician (MLT)': 'MLT',
    'MLT': 'MLT',
    'medical_laboratory': 'MLT',
    'mlt': 'MLT',
}


def get_department_code(department: str) -> str:
    """
    Convert department name to department code.
    
    Args:
        department: Full department name or code
        
    Returns:
        Standardized department code (HIMT, PHT, CHEW, PT, MLT)
        
    Raises:
        ValueError: If department is not recognized
    """
    if not department:
        raise ValueError("Department cannot be empty")
    
    # Try direct lookup first (case-insensitive)
    dept_lower = str(department).lower().strip()
    for key, code in DEPARTMENT_CODES.items():
        if key.lower() == dept_lower:
            return code
    
    # Try partial matching
    for key, code in DEPARTMENT_CODES.items():
        if dept_lower in key.lower() or key.lower() in dept_lower:
            return code
    
    raise ValueError(f"Department '{department}' not recognized. Valid departments: {list(set(DEPARTMENT_CODES.values()))}")


def get_next_sequence_number(dept_code: str, academic_year: str = '2025/2026') -> int:
    """
    Get the next sequence number for a department.
    
    Args:
        dept_code: Department code (HIMT, PHT, CHEW, PT, MLT)
        academic_year: Academic year (default: 2025/2026)
        
    Returns:
        Next sequence number (001, 002, etc.)
    """
    # Query for all matriculation numbers matching pattern: YCHST/{YEAR1}/{YEAR2}/{DEPT_CODE}/###
    # Example: YCHST/2025/2026/PHT/001
    
    pattern = f"YCHST/{academic_year}/{dept_code}/"
    
    last_matric = StudentProfile.objects.filter(
        matriculation_number__startswith=pattern
    ).order_by('-matriculation_number').first()
    
    if last_matric:
        # Parse the sequence number from the last matriculation number
        # Format: YCHST/2025/2026/PHT/001 → extract 001
        try:
            sequence_str = last_matric.matriculation_number.split('/')[-1]
            sequence_num = int(sequence_str)
            return sequence_num + 1
        except (ValueError, IndexError):
            # If parsing fails, default to last count + 1
            count = StudentProfile.objects.filter(
                matriculation_number__startswith=pattern
            ).count()
            return count + 1
    else:
        # No existing matriculation number for this department
        return 1


def generate_matriculation_number(department: str, academic_year: str = '2025/2026') -> str:
    """
    Generate a next matriculation number for a student.
    
    Args:
        department: Full department name or code
        academic_year: Academic year (default: 2025/2026)
        
    Returns:
        Formatted matriculation number
        
    Example:
        >>> generate_matriculation_number('Public Health Technology (PHT)')
        'YCHST/2025/2026/PHT/001'
    """
    # Get standard department code
    dept_code = get_department_code(department)
    
    # Get next sequence number
    next_seq = get_next_sequence_number(dept_code, academic_year)
    
    # Format: YCHST/{ENTRY_YEAR}/{EXIT_YEAR}/{DEPT_CODE}/{SEQUENCE:03d}
    matric_number = f"YCHST/{academic_year}/{dept_code}/{next_seq:03d}"
    
    return matric_number


def validate_matriculation_uniqueness(matric_number: str, exclude_user_id=None) -> bool:
    """
    Check if a matriculation number is unique in the system.
    
    Args:
        matric_number: Matriculation number to validate
        exclude_user_id: User ID to exclude from check (for updates)
        
    Returns:
        True if unique, False otherwise
    """
    query = StudentProfile.objects.filter(matriculation_number=matric_number)
    
    if exclude_user_id:
        query = query.exclude(user_id=exclude_user_id)
    
    return not query.exists()
