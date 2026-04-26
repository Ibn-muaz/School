from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import User
from courses.models import CourseOffering


class Result(models.Model):
    """Student result model"""
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='results')
    course_offering = models.ForeignKey(CourseOffering, on_delete=models.CASCADE, related_name='results')
    
    # Scores
    continuous_assessment = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        validators=[MinValueValidator(0), MaxValueValidator(40)],
        help_text="Continuous assessment score (0-40)"
    )
    examination = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        validators=[MinValueValidator(0), MaxValueValidator(60)],
        help_text="Examination score (0-60)"
    )
    total_score = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Total score (0-100)"
    )
    
    # Grade
    GRADE_CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('E', 'E'),
        ('F', 'F'),
    ]
    
    grade = models.CharField(max_length=1, choices=GRADE_CHOICES)
    
    # Grade point
    grade_point = models.DecimalField(
        max_digits=3, 
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(4)]
    )
    
    # Status
    STATUS_CHOICES = [
        ('pending', 'Pending Moderation'),
        ('approved', 'Approved/Moderated'),
        ('published', 'Published to Student'),
        ('rejected', 'Rejected/Returned'),
    ]
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Approval
    approved_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='approved_results'
    )
    approved_at = models.DateTimeField(null=True, blank=True)
    
    # Remarks
    remarks = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['student', 'course_offering']
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['student', 'status']),
            models.Index(fields=['course_offering', 'status']),
        ]
    
    def __str__(self):
        return f"{self.student.username} - {self.course_offering.course.course_code}: {self.grade}"
    
    def save(self, *args, **kwargs):
        # Calculate total score
        self.total_score = self.continuous_assessment + self.examination
        
        # Calculate grade and grade point
        if self.total_score >= 70:
            self.grade = 'A'
            self.grade_point = 4.00
        elif self.total_score >= 60:
            self.grade = 'B'
            self.grade_point = 3.00
        elif self.total_score >= 50:
            self.grade = 'C'
            self.grade_point = 2.00
        elif self.total_score >= 45:
            self.grade = 'D'
            self.grade_point = 1.00
        elif self.total_score >= 40:
            self.grade = 'E'
            self.grade_point = 0.00
        else:
            self.grade = 'F'
            self.grade_point = 0.00
        
        super().save(*args, **kwargs)


class SemesterResult(models.Model):
    """Semester result summary"""
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='semester_results')
    academic_year = models.CharField(max_length=9, help_text="e.g., 2023/2024")
    semester = models.CharField(max_length=20, choices=[
        ('first', 'First Semester'),
        ('second', 'Second Semester'),
    ])
    
    # GPA calculation
    total_credit_units = models.PositiveIntegerField(default=0)
    total_grade_points = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    gpa = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    
    # Status
    STATUS_CHOICES = [
        ('incomplete', 'Incomplete'),
        ('complete', 'Complete'),
        ('approved', 'Approved'),
    ]
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='incomplete')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['student', 'academic_year', 'semester']
        ordering = ['-academic_year', '-semester']
    
    def __str__(self):
        return f"{self.student.username} - {self.academic_year} {self.get_semester_display()}: {self.gpa}"
    
    def calculate_gpa(self):
        """Calculate GPA based on results"""
        results = Result.objects.filter(
            student=self.student,
            course_offering__academic_year=self.academic_year,
            course_offering__course__semester=self.semester,
            status='approved'
        )
        
        total_credits = 0
        total_points = 0
        
        for result in results:
            credit_units = result.course_offering.course.credit_units
            total_credits += credit_units
            total_points += result.grade_point * credit_units
        
        if total_credits > 0:
            self.total_credit_units = total_credits
            self.total_grade_points = total_points
            self.gpa = total_points / total_credits
            self.status = 'complete'
        else:
            self.status = 'incomplete'
        
        self.save()


class Transcript(models.Model):
    """Student transcript model"""
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transcripts')
    
    # Transcript details
    transcript_type = models.CharField(max_length=20, choices=[
        ('interim', 'Interim Transcript'),
        ('final', 'Final Transcript'),
    ], default='interim')
    
    # Academic summary
    total_credits_earned = models.PositiveIntegerField(default=0)
    cgpa = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    class_of_degree = models.CharField(max_length=50, blank=True)
    
    # Status
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('generated', 'Generated'),
        ('approved', 'Approved'),
    ]
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # File
    transcript_file = models.FileField(upload_to='transcripts/', null=True, blank=True)
    
    # Request and approval
    requested_at = models.DateTimeField(auto_now_add=True)
    generated_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='generated_transcripts'
    )
    generated_at = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-requested_at']
    
    def __str__(self):
        return f"{self.student.username} - {self.get_transcript_type_display()} Transcript"