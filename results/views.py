from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Result, SemesterResult, Transcript
from .serializers import ResultSerializer, SemesterResultSerializer, TranscriptSerializer


class ResultListView(generics.ListAPIView):
    """List results"""
    serializer_class = ResultSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        
        if user.role == 'student':
            # Students see their own results
            return Result.objects.filter(student=user, status='published')
        elif user.role == 'staff':
            # Staff see results for courses they teach
            return Result.objects.filter(
                course_offering__lecturer=user,
                status__in=['pending', 'approved', 'published']
            )
        else:
            return Result.objects.none()


class ResultDetailView(generics.RetrieveUpdateAPIView):
    """Retrieve and update result"""
    serializer_class = ResultSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        
        if user.role == 'student':
            return Result.objects.filter(student=user, status='published')
        elif user.role == 'staff':
            return Result.objects.filter(course_offering__lecturer=user)
        else:
            return Result.objects.none()
    
    def perform_update(self, serializer):
        if self.request.user.role == 'staff':
            serializer.save(approved_by=self.request.user)


class SemesterResultListView(generics.ListAPIView):
    """List semester results"""
    serializer_class = SemesterResultSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return SemesterResult.objects.filter(student=self.request.user)


class TranscriptListCreateView(generics.ListCreateAPIView):
    """List and create transcript requests"""
    serializer_class = TranscriptSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Transcript.objects.filter(student=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(student=self.request.user)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def student_results_dashboard(request):
    """Student results dashboard"""
    if request.user.role != 'student':
        return Response({'error': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
    
    user = request.user
    
    # Get current semester results
    semester = request.query_params.get('semester', 'first')
    academic_year = request.query_params.get('academic_year', '2023/2024')
    
    results = Result.objects.filter(
        student=user,
        course_offering__academic_year=academic_year,
        course_offering__course__semester=semester,
        status='published'
    )
    
    # Get semester result
    try:
        semester_result = SemesterResult.objects.get(
            student=user,
            academic_year=academic_year,
            semester=semester
        )
    except SemesterResult.DoesNotExist:
        semester_result = None
    
    # Calculate CGPA (simplified - should be more complex in real implementation)
    all_results = Result.objects.filter(
        student=user,
        status='published'
    )
    
    total_credits = 0
    total_points = 0
    
    for result in all_results:
        credits = result.course_offering.course.credit_units
        total_credits += credits
        total_points += result.grade_point * credits
    
    cgpa = total_points / total_credits if total_credits > 0 else 0
    
    data = {
        'current_semester': {
            'semester': semester,
            'academic_year': academic_year,
            'results': ResultSerializer(results, many=True).data,
            'semester_gpa': semester_result.gpa if semester_result else 0,
        },
        'academic_summary': {
            'total_credits_earned': total_credits,
            'cgpa': round(cgpa, 2),
        },
    }
    
    return Response(data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def approve_result(request, result_id):
    """Approve a result (staff only)"""
    if request.user.role != 'staff':
        return Response({'error': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        result = Result.objects.get(id=result_id, course_offering__lecturer=request.user)
    except Result.DoesNotExist:
        return Response({'error': 'Result not found'}, status=status.HTTP_404_NOT_FOUND)
    
    result.status = 'approved'
    result.approved_by = request.user
    result.save()
    
    return Response({'message': 'Result approved successfully'})


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def publish_results(request):
    """Publish results for a course (staff only)"""
    if request.user.role != 'staff':
        return Response({'error': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
    
    course_offering_id = request.data.get('course_offering_id')
    
    if not course_offering_id:
        return Response({'error': 'Course offering ID is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Update all approved results for this course offering to published
    updated_count = Result.objects.filter(
        course_offering_id=course_offering_id,
        course_offering__lecturer=request.user,
        status='approved'
    ).update(status='published')
    
    return Response({
        'message': f'Successfully published {updated_count} results'
    })