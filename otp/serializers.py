from rest_framework import serializers
from .models import OTPSettings, OTPAttempt, OTPBlacklist


class OTPSettingsSerializer(serializers.ModelSerializer):
    """Serializer for OTPSettings model"""
    
    class Meta:
        model = OTPSettings
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'updated_at']


class OTPAttemptSerializer(serializers.ModelSerializer):
    """Serializer for OTPAttempt model"""
    
    class Meta:
        model = OTPAttempt
        fields = '__all__'


class OTPBlacklistSerializer(serializers.ModelSerializer):
    """Serializer for OTPBlacklist model"""
    
    class Meta:
        model = OTPBlacklist
        fields = '__all__'