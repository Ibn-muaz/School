from rest_framework import serializers
from .models import Result, SemesterResult, Transcript


class ResultSerializer(serializers.ModelSerializer):
    """Serializer for Result model"""
    course_code = serializers.CharField(source='course_offering.course.course_code', read_only=True)
    course_title = serializers.CharField(source='course_offering.course.course_title', read_only=True)
    credit_units = serializers.IntegerField(source='course_offering.course.credit_units', read_only=True)
    academic_year = serializers.CharField(source='course_offering.academic_year', read_only=True)
    semester = serializers.CharField(source='course_offering.course.semester', read_only=True)
    lecturer_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Result
        fields = '__all__'
        read_only_fields = ['student', 'approved_by', 'approved_at', 'created_at', 'updated_at']
    
    def get_lecturer_name(self, obj):
        lecturer = obj.course_offering.lecturer
        return lecturer.get_full_name() if lecturer else None


class SemesterResultSerializer(serializers.ModelSerializer):
    """Serializer for SemesterResult model"""
    
    class Meta:
        model = SemesterResult
        fields = '__all__'
        read_only_fields = ['student', 'created_at', 'updated_at']


class TranscriptSerializer(serializers.ModelSerializer):
    """Serializer for Transcript model"""
    
    class Meta:
        model = Transcript
        fields = '__all__'
        read_only_fields = ['student', 'generated_by', 'generated_at', 'requested_at', 'updated_at']