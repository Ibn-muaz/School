from rest_framework import serializers
from .models import Hostel, Room, BedSpace, HostelAllocation
from accounts.models import User


class HostelSerializer(serializers.ModelSerializer):
    """Serialize hostel information"""
    available_beds = serializers.SerializerMethodField()
    
    class Meta:
        model = Hostel
        fields = ['id', 'name', 'gender_category', 'location', 'description', 
                  'price_per_session', 'available_beds']
    
    def get_available_beds(self, obj):
        """Count available bed spaces"""
        return BedSpace.objects.filter(
            room__hostel=obj,
            allocation__isnull=True
        ).count()


class BedSpaceSerializer(serializers.ModelSerializer):
    """Serialize individual bed spaces"""
    room_number = serializers.CharField(source='room.room_number', read_only=True)
    hostel_name = serializers.CharField(source='room.hostel.name', read_only=True)
    bed_identifier = serializers.CharField(read_only=True)
    
    class Meta:
        model = BedSpace
        fields = ['id', 'bed_identifier', 'room_number', 'hostel_name', 'is_available']


class RoomSerializer(serializers.ModelSerializer):
    """Serialize room information with bed spaces"""
    hostel_name = serializers.CharField(source='hostel.name', read_only=True)
    beds = BedSpaceSerializer(source='bed_spaces', many=True, read_only=True)
    
    class Meta:
        model = Room
        fields = ['id', 'room_number', 'floor', 'capacity', 'hostel_name', 'beds']


class HostelAllocationSerializer(serializers.ModelSerializer):
    """Serialize hostel allocation records"""
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    student_id = serializers.CharField(source='student.id', read_only=True)
    bed_identifier = serializers.CharField(source='bed_space.bed_identifier', read_only=True)
    room_number = serializers.CharField(source='bed_space.room.room_number', read_only=True)
    hostel_name = serializers.CharField(source='bed_space.room.hostel.name', read_only=True)
    fee_amount = serializers.FloatField(
        source='bed_space.room.hostel.price_per_session',
        read_only=True
    )
    
    class Meta:
        model = HostelAllocation
        fields = ['id', 'student_id', 'student_name', 'bed_identifier', 'room_number', 
                  'hostel_name', 'status', 'fee_amount', 'allocated_at', 'payment_date']
        read_only_fields = ['allocated_at', 'payment_date', 'student_name', 'student_id']


class StudentAllocationDetailSerializer(serializers.ModelSerializer):
    """Student-specific allocation details for dashboard"""
    hostel_name = serializers.CharField(source='bed_space.room.hostel.name', read_only=True)
    room_number = serializers.CharField(source='bed_space.room.room_number', read_only=True)
    bed_identifier = serializers.CharField(source='bed_space.bed_identifier', read_only=True)
    floor = serializers.CharField(source='bed_space.room.floor', read_only=True)
    price_per_session = serializers.FloatField(
        source='bed_space.room.hostel.price_per_session',
        read_only=True
    )
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = HostelAllocation
        fields = ['id', 'hostel_name', 'room_number', 'bed_identifier', 'floor', 
                  'status', 'status_display', 'price_per_session', 'allocated_at', 
                  'payment_date']
        read_only_fields = fields
