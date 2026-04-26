from rest_framework import serializers
from .models import CourseRegistration, ProgramChange, IndexingRequest


class CourseRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for CourseRegistration model"""
    
    class Meta:
        model = CourseRegistration
        fields = '__all__'
        read_only_fields = ['student', 'registered_at', 'updated_at']


class ProgramChangeSerializer(serializers.ModelSerializer):
    """Serializer for ProgramChange model"""
    
    class Meta:
        model = ProgramChange
        fields = '__all__'
        read_only_fields = ['student', 'approved_by', 'approved_at', 'requested_at', 'updated_at']


class IndexingRequestSerializer(serializers.ModelSerializer):
    """Serializer for IndexingRequest model"""
    
    class Meta:
        model = IndexingRequest
        fields = '__all__'
        read_only_fields = ['student', 'processed_by', 'processed_at', 'requested_at', 'updated_at']