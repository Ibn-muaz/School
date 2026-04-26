from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, StudentProfile, StaffProfile


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Custom admin for User model"""
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_active', 'date_joined')
    list_filter = ('role', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    
    fieldsets = UserAdmin.fieldsets + (
        ('Role Information', {
            'fields': ('role', 'phone_number', 'date_of_birth', 'address', 'profile_picture', 'is_otp_verified',
                       'must_change_password')
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Role Information', {
            'fields': ('role', 'phone_number', 'date_of_birth', 'address', 'profile_picture',
                       'must_change_password')
        }),
    )


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    """Admin for StudentProfile model"""
    list_display = ('user', 'matriculation_number', 'department_code', 'department', 'level', 'is_active')
    list_filter = ('department_code', 'level', 'is_active', 'admission_year')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'matriculation_number')
    readonly_fields = ('total_fees_paid',)


@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):
    """Admin for StaffProfile model"""
    list_display = ('user', 'staff_id', 'department', 'current_rank', 'is_active')
    list_filter = ('department_code', 'current_rank', 'is_active')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'staff_id')