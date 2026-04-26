from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Course, CourseOffering
from .serializers import CourseSerializer, CourseOfferingSerializer


class CourseListView(generics.ListAPIView):
    """List all courses"""
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = Course.objects.filter(is_active=True)
        
        # Filter by level if provided
        level = self.request.query_params.get('level')
        if level:
            queryset = queryset.filter(level=level)
        
        # Filter by semester if provided
        semester = self.request.query_params.get('semester')
        if semester:
            queryset = queryset.filter(semester=semester)
        
        # Filter by department if provided
        department = self.request.query_params.get('department')
        if department:
            queryset = queryset.filter(department=department)
        
        return queryset


class CourseDetailView(generics.RetrieveAPIView):
    """Retrieve course details"""
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Course.objects.filter(is_active=True)


class CourseOfferingListView(generics.ListAPIView):
    """List course offerings"""
    serializer_class = CourseOfferingSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = CourseOffering.objects.filter(is_active=True)
        
        # Filter by academic year
        academic_year = self.request.query_params.get('academic_year', '2023/2024')
        queryset = queryset.filter(academic_year=academic_year)
        
        # Filter by lecturer if staff user
        if self.request.user.role == 'staff':
            queryset = queryset.filter(lecturer=self.request.user)
        
        return queryset


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def course_catalog(request):
    """Course catalog for students"""
    if request.user.role != 'student':
        return Response({'error': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        profile = request.user.student_profile
    except:
        return Response({'error': 'Student profile not found'}, status=400)
    
    # Get courses for student's level and semester
    semester = request.query_params.get('semester', 'first')
    academic_year = request.query_params.get('academic_year', '2023/2024')
    
    courses = Course.objects.filter(
        level=profile.level,
        semester=semester,
        is_active=True
    )
    
    # Get offerings for these courses
    course_codes = courses.values_list('course_code', flat=True)
    offerings = CourseOffering.objects.filter(
        course__course_code__in=course_codes,
        academic_year=academic_year,
        is_active=True
    )
    
    data = {
        'student_level': profile.level,
        'semester': semester,
        'academic_year': academic_year,
        'available_courses': CourseSerializer(courses, many=True).data,
        'course_offerings': CourseOfferingSerializer(offerings, many=True).data,
    }
    
    return Response(data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def lecturer_courses(request):
    """Courses assigned to lecturer"""
    if request.user.role != 'staff':
        return Response({'error': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
    
    academic_year = request.query_params.get('academic_year', '2023/2024')
    
    offerings = CourseOffering.objects.filter(
        lecturer=request.user,
        academic_year=academic_year,
        is_active=True
    )
    
    data = {
        'lecturer': request.user.get_full_name(),
        'academic_year': academic_year,
        'assigned_courses': CourseOfferingSerializer(offerings, many=True).data,
    }
    
    return Response(data)