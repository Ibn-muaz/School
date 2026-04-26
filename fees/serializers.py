from rest_framework import serializers
from .models import FeeStructure, FeePayment, OtherPayment


class FeeStructureSerializer(serializers.ModelSerializer):
    """Serializer for FeeStructure model"""
    
    class Meta:
        model = FeeStructure
        fields = '__all__'


class FeePaymentSerializer(serializers.ModelSerializer):
    """Serializer for FeePayment model"""
    
    class Meta:
        model = FeePayment
        fields = '__all__'
        read_only_fields = ['student', 'payment_date', 'verified_by', 'verified_at', 'updated_at']


class OtherPaymentSerializer(serializers.ModelSerializer):
    """Serializer for OtherPayment model"""
    
    class Meta:
        model = OtherPayment
        fields = '__all__'
        read_only_fields = ['student', 'payment_date', 'verified_by', 'verified_at', 'updated_at']