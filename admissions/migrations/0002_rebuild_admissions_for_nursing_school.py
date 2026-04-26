# Generated migration - Rebuild admissions models for real nursing school portal

from django.db import migrations, models
import django.db.models.deletion
import django.core.validators
from django.utils import timezone


class Migration(migrations.Migration):

    dependencies = [
        ('admissions', '0001_initial'),
        ('accounts', '0006_update_user_roles'),
    ]

    operations = [
        # Remove old fields and add comprehensive new ones
        migrations.RemoveField(
            model_name='applicantprofile',
            name='religion',
        ),
        
        # ApplicantProfile updates
        migrations.AddField(
            model_name='applicantprofile',
            name='date_of_birth',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='applicantprofile',
            name='phone_number',
            field=models.CharField(max_length=20, blank=True),
        ),
        migrations.AddField(
            model_name='applicantprofile',
            name='alternative_phone',
            field=models.CharField(max_length=20, blank=True),
        ),
        migrations.AddField(
            model_name='applicantprofile',
            name='residential_address',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='applicantprofile',
            name='gender',
            field=models.CharField(
                blank=True,
                choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')],
                max_length=10,
            ),
        ),
        migrations.AddField(
            model_name='applicantprofile',
            name='blood_group',
            field=models.CharField(
                blank=True,
                choices=[
                    ('O+', 'O+'),
                    ('O-', 'O-'),
                    ('A+', 'A+'),
                    ('A-', 'A-'),
                    ('B+', 'B+'),
                    ('B-', 'B-'),
                    ('AB+', 'AB+'),
                    ('AB-', 'AB-'),
                ],
                max_length=5,
            ),
        ),
        migrations.AddField(
            model_name='applicantprofile',
            name='has_medical_conditions',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='applicantprofile',
            name='medical_conditions_details',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='applicantprofile',
            name='has_disabilities',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='applicantprofile',
            name='disability_details',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='applicantprofile',
            name='vaccinations_up_to_date',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='applicantprofile',
            name='nok_relationship',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='applicantprofile',
            name='is_employed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='applicantprofile',
            name='employment_details',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='applicantprofile',
            name='has_healthcare_experience',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='applicantprofile',
            name='healthcare_experience_details',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='applicantprofile',
            name='profile_completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='applicantprofile',
            name='profile_completed_at',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='applicantprofile',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='applicantprofile',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        
        # AcademicHistory updates
        migrations.AlterModelOptions(
            name='academichistory',
            options={'verbose_name': 'Academic History', 'verbose_name_plural': 'Academic Histories'},
        ),
        migrations.AddField(
            model_name='academichistory',
            name='secondary_school_name',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='academichistory',
            name='secondary_school_type',
            field=models.CharField(
                blank=True,
                choices=[
                    ('public', 'Public School'),
                    ('private', 'Private School'),
                    ('tsc', 'Teachers Training College'),
                    ('other', 'Other'),
                ],
                max_length=50,
            ),
        ),
        migrations.AddField(
            model_name='academichistory',
            name='secondary_school_state',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='academichistory',
            name='year_graduated',
            field=models.PositiveIntegerField(
                blank=True,
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(1990),
                    django.core.validators.MaxValueValidator(2030),
                ],
            ),
        ),
        migrations.RenameField(
            model_name='academichistory',
            old_name='sitting_count',
            new_name='olevel_sitting_count',
        ),
        migrations.AddField(
            model_name='academichistory',
            name='olevel_exam_type',
            field=models.CharField(
                choices=[('WAEC', 'WAEC'), ('NECO', 'NECO'), ('NABTEB', 'NABTEB'), ('GCE', 'GCE')],
                default='WAEC',
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name='academichistory',
            name='olevel_exam_year',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='academichistory',
            name='jamb_reg_number',
            field=models.CharField(blank=True, max_length=20, unique=True),
        ),
        migrations.AddField(
            model_name='academichistory',
            name='jamb_exam_year',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='academichistory',
            name='jamb_score',
            field=models.PositiveIntegerField(
                blank=True,
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(400),
                ],
            ),
        ),
        migrations.AddField(
            model_name='academichistory',
            name='jamb_subject_combination',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='academichistory',
            name='entry_type',
            field=models.CharField(
                choices=[('utme', 'UTME'), ('direct_entry', 'Direct Entry'), ('transfer', 'Transfer')],
                default='utme',
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name='academichistory',
            name='previous_institution',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='academichistory',
            name='previous_program',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='academichistory',
            name='previous_level',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='academichistory',
            name='previous_cgpa',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True),
        ),
        migrations.AddField(
            model_name='academichistory',
            name='has_olevel_transcript',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='academichistory',
            name='has_jamb_result_slip',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='academichistory',
            name='has_birth_certificate',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='academichistory',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='academichistory',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        
        # ApplicationRecord updates
        migrations.AlterField(
            model_name='applicationrecord',
            name='status',
            field=models.CharField(
                choices=[
                    ('not_started', 'Not Started'),
                    ('profile_started', 'Profile In Progress'),
                    ('profile_complete', 'Profile Complete'),
                    ('education_started', 'Education Info In Progress'),
                    ('education_complete', 'Education Complete'),
                    ('documents_started', 'Documents In Progress'),
                    ('documents_complete', 'Documents Complete'),
                    ('submitted', 'Application Submitted'),
                    ('payment_pending', 'Awaiting Payment'),
                    ('payment_confirmed', 'Payment Confirmed'),
                    ('under_review', 'Under Review'),
                    ('interview_scheduled', 'Interview Scheduled'),
                    ('interview_completed', 'Interview Completed'),
                    ('admitted', 'Admitted'),
                    ('waitlisted', 'Waitlisted'),
                    ('rejected', 'Not Admitted'),
                    ('deferred', 'Application Deferred'),
                ],
                default='not_started',
                max_length=25,
            ),
        ),
        migrations.AlterField(
            model_name='applicationrecord',
            name='first_choice_program',
            field=models.CharField(
                blank=True,
                choices=[
                    ('pht', 'Public Health Technology'),
                    ('himt', 'Health Information Management Technology'),
                    ('chew', 'Community Health Extension Workers'),
                    ('pt', 'Pharmacy Technician'),
                    ('mlt', 'Medical Laboratory Technician'),
                ],
                max_length=4,
            ),
        ),
        migrations.AlterField(
            model_name='applicationrecord',
            name='second_choice_program',
            field=models.CharField(
                blank=True,
                choices=[
                    ('pht', 'Public Health Technology'),
                    ('himt', 'Health Information Management Technology'),
                    ('chew', 'Community Health Extension Workers'),
                    ('pt', 'Pharmacy Technician'),
                    ('mlt', 'Medical Laboratory Technician'),
                ],
                max_length=4,
            ),
        ),
        migrations.AddField(
            model_name='applicationrecord',
            name='application_fee',
            field=models.DecimalField(decimal_places=2, default=5000.0, max_digits=10),
        ),
        migrations.AddField(
            model_name='applicationrecord',
            name='payment_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='applicationrecord',
            name='admission_decision',
            field=models.CharField(
                blank=True,
                choices=[
                    ('admitted', 'Admitted'),
                    ('rejected', 'Rejected'),
                    ('waitlisted', 'Waitlisted'),
                ],
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name='applicationrecord',
            name='admission_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='applicationrecord',
            name='admission_notes',
            field=models.TextField(blank=True),
        ),
        
        # AdmissionDocument updates
        migrations.AlterField(
            model_name='admissiondocument',
            name='document_type',
            field=models.CharField(
                choices=[
                    ('passport_photo', 'Passport Photograph (4x6)'),
                    ('olevel_transcript', 'O-Level Statement of Result'),
                    ('jamb_result_slip', 'JAMB Result Slip'),
                    ('jamb_printout', 'JAMB Admission Printout'),
                    ('birth_certificate', 'Birth Certificate / Age Declaration'),
                    ('indigene_certificate', 'Local Government Indigene Certificate'),
                    ('national_id', 'National ID Card'),
                    ('drivers_license', "Driver's License"),
                    ('medical_report', 'Pre-admission Medical Report'),
                    ('vaccination_card', 'Vaccination Record'),
                    ('other', 'Other Supporting Document'),
                ],
                max_length=30,
            ),
        ),
        migrations.AddField(
            model_name='admissiondocument',
            name='file_size',
            field=models.PositiveIntegerField(default=0, help_text='File size in bytes'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='admissiondocument',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='admissiondocument',
            name='verification_notes',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='admissiondocument',
            name='verified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='verified_documents', to='accounts.user'),
        ),
        migrations.AddField(
            model_name='admissiondocument',
            name='verified_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='admissiondocument',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='admissiondocument',
            name='file',
            field=models.FileField(upload_to='admission_docs/%Y/%m/%d/'),
        ),
        migrations.AlterUniqueTogether(
            name='admissiondocument',
            unique_together={('application', 'document_type')},
        ),
        
        # New models
        migrations.CreateModel(
            name='ApplicationStatusHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('old_status', models.CharField(blank=True, max_length=25)),
                ('new_status', models.CharField(max_length=25)),
                ('notes', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history', to='admissions.applicationrecord')),
                ('changed_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.user')),
            ],
            options={
                'verbose_name_plural': 'Application Status Histories',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='InterviewSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('scheduled', 'Scheduled'), ('completed', 'Completed'), ('no_show', 'No Show'), ('rescheduled', 'Rescheduled')], default='scheduled', max_length=20)),
                ('interview_date', models.DateTimeField()),
                ('interview_venue', models.CharField(blank=True, max_length=200)),
                ('interviewer_name', models.CharField(blank=True, max_length=100)),
                ('score', models.PositiveIntegerField(blank=True, help_text='Interview score out of 100', null=True, validators=[django.core.validators.MaxValueValidator(100)])),
                ('feedback', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='interviews', to='admissions.applicationrecord')),
            ],
            options={
                'ordering': ['-interview_date'],
            },
        ),
    ]
