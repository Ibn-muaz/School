from django.db import models
from accounts.models import User


class Course(models.Model):
    """Course model"""
    
    course_code = models.CharField(max_length=10, unique=True)
    course_title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    # Course details
    credit_units = models.PositiveIntegerField()
    level = models.CharField(max_length=10, help_text="Student level: 100, 200, 300, 400")
    semester = models.CharField(max_length=20, choices=[
        ('first', 'First Semester'),
        ('second', 'Second Semester'),
    ])
    
    # Department and faculty
    department = models.CharField(max_length=100)
    faculty = models.CharField(max_length=100)
    
    # Prerequisites
    prerequisites = models.ManyToManyField('self', blank=True, symmetrical=False)
    
    # Status
    is_active = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['course_code']
        indexes = [
            models.Index(fields=['level', 'semester']),
            models.Index(fields=['department']),
        ]
    
    def __str__(self):
        return f"{self.course_code} - {self.course_title}"


class CourseOffering(models.Model):
    """Course offering model for specific academic years"""
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='offerings')
    academic_year = models.CharField(max_length=9, help_text="e.g., 2023/2024")
    
    # Lecturer assignment
    lecturer = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='courses_taught'
    )
    
    # Class details
    class_capacity = models.PositiveIntegerField(default=50)
    enrolled_students = models.PositiveIntegerField(default=0)
    
    # Schedule (optional)
    day_of_week = models.CharField(max_length=10, choices=[
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
    ], blank=True)
    
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    venue = models.CharField(max_length=100, blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['course', 'academic_year']
        ordering = ['course__course_code']
    
    def __str__(self):
        return f"{self.course.course_code} ({self.academic_year})"
    
    @property
    def available_slots(self):
        return max(0, self.class_capacity - self.enrolled_students)