from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from accounts.models import User
from .models import CourseRegistration, ProgramChange, IndexingRequest
from .serializers import (
    CourseRegistrationSerializer, ProgramChangeSerializer, 
    IndexingRequestSerializer
)


class CourseRegistrationListCreateView(generics.ListCreateAPIView):
    """List and create course registrations"""
    serializer_class = CourseRegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return CourseRegistration.objects.filter(student=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(student=self.request.user)


class CourseRegistrationDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, and delete course registration"""
    serializer_class = CourseRegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return CourseRegistration.objects.filter(student=self.request.user)


class ProgramChangeListCreateView(generics.ListCreateAPIView):
    """List and create program change requests"""
    serializer_class = ProgramChangeSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return ProgramChange.objects.filter(student=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(student=self.request.user)


class ProgramChangeDetailView(generics.RetrieveUpdateAPIView):
    """Retrieve and update program change request"""
    serializer_class = ProgramChangeSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return ProgramChange.objects.filter(student=self.request.user)


class IndexingRequestListCreateView(generics.ListCreateAPIView):
    """List and create indexing requests"""
    serializer_class = IndexingRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return IndexingRequest.objects.filter(student=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(student=self.request.user)


class IndexingRequestDetailView(generics.RetrieveUpdateAPIView):
    """Retrieve and update indexing request"""
    serializer_class = IndexingRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return IndexingRequest.objects.filter(student=self.request.user)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def student_dashboard(request):
    """Student dashboard data"""
    user = request.user
    
    # Get student profile
    try:
        profile = user.student_profile
    except:
        return Response({'error': 'Student profile not found'}, status=400)
    
    # Get course registrations for current semester
    current_semester = 'first'  # This should be configurable
    current_year = '2023/2024'  # This should be configurable
    
    course_registrations = CourseRegistration.objects.filter(
        student=user,
        semester=current_semester,
        academic_year=current_year
    )
    
    # Get pending requests
    pending_program_changes = ProgramChange.objects.filter(
        student=user, 
        status='pending'
    ).count()
    
    pending_indexing = IndexingRequest.objects.filter(
        student=user, 
        status__in=['pending', 'processing']
    ).count()
    
    data = {
        'profile': {
            'matriculation_number': profile.matriculation_number,
            'department': profile.department,
            'faculty': profile.faculty,
            'level': profile.level,
            'program': profile.program,
            'total_fees_paid': profile.total_fees_paid,
        },
        'current_semester': {
            'semester': current_semester,
            'year': current_year,
            'registered_courses': course_registrations.count(),
            'total_credits': sum(reg.credit_units for reg in course_registrations),
        },
        'pending_requests': {
            'program_changes': pending_program_changes,
            'indexing_requests': pending_indexing,
        }
    }
    
    return Response(data)