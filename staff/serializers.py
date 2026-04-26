from rest_framework import serializers
from .models import CourseAllocation, Scoresheet, SalaryRecord


class CourseAllocationSerializer(serializers.ModelSerializer):
    """Serializer for CourseAllocation model"""
    
    class Meta:
        model = CourseAllocation
        fields = '__all__'
        read_only_fields = ['staff', 'allocated_at']


class ScoresheetSerializer(serializers.ModelSerializer):
    """Serializer for Scoresheet model"""
    
    class Meta:
        model = Scoresheet
        fields = '__all__'
        read_only_fields = ['uploaded_by', 'approved_by', 'approved_at', 'uploaded_at', 'updated_at']


class SalaryRecordSerializer(serializers.ModelSerializer):
    """Serializer for SalaryRecord model"""
    
    class Meta:
        model = SalaryRecord
        fields = '__all__'
        read_only_fields = ['staff', 'created_at', 'updated_at']