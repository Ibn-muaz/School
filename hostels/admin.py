from django.contrib import admin
from .models import Hostel, Room, BedSpace, HostelAllocation


@admin.register(Hostel)
class HostelAdmin(admin.ModelAdmin):
    list_display = ['name', 'gender_category', 'location', 'price_per_session']
    list_filter = ['gender_category']
    search_fields = ['name', 'location']


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['room_number', 'floor', 'hostel', 'capacity']
    list_filter = ['hostel', 'floor']
    search_fields = ['room_number', 'hostel__name']


@admin.register(BedSpace)
class BedSpaceAdmin(admin.ModelAdmin):
    list_display = ['bed_identifier', 'room', 'room_hostel']
    list_filter = ['room__hostel', 'room__floor']
    search_fields = ['bed_identifier', 'room__room_number']
    
    def room_hostel(self, obj):
        return obj.room.hostel.name
    room_hostel.short_description = 'Hostel'


@admin.register(HostelAllocation)
class HostelAllocationAdmin(admin.ModelAdmin):
    list_display = ['student', 'bed_identifier', 'status', 'allocated_at', 'payment_date']
    list_filter = ['status', 'allocated_at']
    search_fields = ['student__username', 'student__email', 'bed_space__bed_identifier']
    readonly_fields = ['allocated_at', 'payment_date']
    
    fieldsets = (
        ('Student Information', {
            'fields': ('student',)
        }),
        ('Allocation Details', {
            'fields': ('bed_space', 'status')
        }),
        ('Timestamps', {
            'fields': ('allocated_at', 'payment_date'),
            'classes': ('collapse',)
        }),
    )
    
    def bed_identifier(self, obj):
        return obj.bed_space.bed_identifier
    bed_identifier.short_description = 'Bed'
