from rest_framework import serializers
from .models import OTPRecord


class OTPRecordSerializer(serializers.ModelSerializer):
    """Serializer for OTPRecord model"""
    user_full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = OTPRecord
        fields = '__all__'
    
    def get_user_full_name(self, obj):
        return obj.user.get_full_name()