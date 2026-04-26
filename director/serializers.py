from rest_framework import serializers
from .models import PermissionRequest, SalaryVerification


class PermissionRequestSerializer(serializers.ModelSerializer):
    """Serializer for PermissionRequest model"""
    requested_by_name = serializers.SerializerMethodField()
    approved_by_name = serializers.SerializerMethodField()
    
    class Meta:
        model = PermissionRequest
        fields = '__all__'
    
    def get_requested_by_name(self, obj):
        return obj.requested_by.get_full_name()
    
    def get_approved_by_name(self, obj):
        return obj.approved_by.get_full_name() if obj.approved_by else None


class SalaryVerificationSerializer(serializers.ModelSerializer):
    """Serializer for SalaryVerification model"""
    staff_name = serializers.SerializerMethodField()
    processed_by_name = serializers.SerializerMethodField()
    
    class Meta:
        model = SalaryVerification
        fields = '__all__'
    
    def get_staff_name(self, obj):
        return obj.staff.get_full_name()
    
    def get_processed_by_name(self, obj):
        return obj.processed_by.get_full_name() if obj.processed_by else None