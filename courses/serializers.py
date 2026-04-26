from rest_framework import serializers
from .models import Course, CourseOffering


class CourseSerializer(serializers.ModelSerializer):
    """Serializer for Course model"""
    
    class Meta:
        model = Course
        fields = '__all__'


class CourseOfferingSerializer(serializers.ModelSerializer):
    """Serializer for CourseOffering model"""
    course_code = serializers.CharField(source='course.course_code', read_only=True)
    course_title = serializers.CharField(source='course.course_title', read_only=True)
    credit_units = serializers.IntegerField(source='course.credit_units', read_only=True)
    lecturer_name = serializers.SerializerMethodField()
    
    class Meta:
        model = CourseOffering
        fields = '__all__'
    
    def get_lecturer_name(self, obj):
        return obj.lecturer.get_full_name() if obj.lecturer else None