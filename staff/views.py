from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from accounts.models import User
from .models import CourseAllocation, Scoresheet, SalaryRecord
from .serializers import (
    CourseAllocationSerializer, ScoresheetSerializer, 
    SalaryRecordSerializer
)


class CourseAllocationListView(generics.ListAPIView):
    """List course allocations for staff"""
    serializer_class = CourseAllocationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return CourseAllocation.objects.filter(staff=self.request.user, is_active=True)


class ScoresheetListCreateView(generics.ListCreateAPIView):
    """List and create scoresheets"""
    serializer_class = ScoresheetSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Scoresheet.objects.filter(uploaded_by=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)


class ScoresheetDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, and delete scoresheet"""
    serializer_class = ScoresheetSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Scoresheet.objects.filter(uploaded_by=self.request.user)


class SalaryRecordListView(generics.ListAPIView):
    """List salary records for staff"""
    serializer_class = SalaryRecordSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return SalaryRecord.objects.filter(staff=self.request.user)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def staff_dashboard(request):
    """Staff dashboard data"""
    user = request.user
    
    # Get staff profile
    try:
        profile = user.staff_profile
    except:
        return Response({'error': 'Staff profile not found'}, status=400)
    
    # Get current course allocations
    current_allocations = CourseAllocation.objects.filter(
        staff=user, 
        is_active=True
    )
    
    # Get recent scoresheets
    recent_scoresheets = Scoresheet.objects.filter(
        uploaded_by=user
    ).order_by('-uploaded_at')[:5]
    
    # Get latest salary record
    latest_salary = SalaryRecord.objects.filter(
        staff=user
    ).order_by('-year', '-month').first()
    
    data = {
        'profile': {
            'staff_id': profile.staff_id,
            'department': profile.department,
            'faculty': profile.faculty,
            'current_rank': profile.get_current_rank_display(),
            'basic_salary': profile.basic_salary,
        },
        'current_allocations': CourseAllocationSerializer(current_allocations, many=True).data,
        'recent_scoresheets': ScoresheetSerializer(recent_scoresheets, many=True).data,
        'latest_salary': SalaryRecordSerializer(latest_salary).data if latest_salary else None,
    }
    
    return Response(data)