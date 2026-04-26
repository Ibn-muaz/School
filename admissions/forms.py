from django import forms
from django.contrib.auth import authenticate
from .models import ApplicationRecord, ApplicantProfile, AcademicHistory, AdmissionDocument
from accounts.models import User
from datetime import datetime, timedelta


class ApplicantSignupForm(forms.ModelForm):
    """Registration form for new applicants"""
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Create a strong password'
        }),
        min_length=8,
        help_text="Minimum 8 characters"
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm password'
        }),
        label="Confirm Password"
    )
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First Name',
                'required': True
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last Name',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your.email@example.com',
                'required': True
            }),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")
        
        email = cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        
        return cleaned_data


class ApplicantProfileForm(forms.ModelForm):
    """Personal and biographical information for applicants"""
    
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'max': str(datetime.now().date())
        }),
        required=True,
        help_text="You must be at least 16 years old"
    )
    
    class Meta:
        model = ApplicantProfile
        fields = [
            'date_of_birth', 'phone_number', 'alternative_phone', 'gender',
            'residential_address', 'state_of_origin', 'lga',
            'blood_group', 'genotype',
            'has_medical_conditions', 'medical_conditions_details',
            'has_disabilities', 'disability_details',
            'vaccinations_up_to_date',
            'is_employed', 'employment_details',
            'has_healthcare_experience', 'healthcare_experience_details',
            'nok_name', 'nok_relationship', 'nok_phone', 'nok_address'
        ]
        widgets = {
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '08012345678',
                'pattern': '[0-9]{10,}',
                'required': True
            }),
            'alternative_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Optional'
            }),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'residential_address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Your residential address'
            }),
            'state_of_origin': forms.Select(attrs={'class': 'form-control'}),
            'lga': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Local Government Area'
            }),
            'blood_group': forms.Select(attrs={'class': 'form-control'}),
            'genotype': forms.Select(attrs={'class': 'form-control'}),
            'medical_conditions_details': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Describe any medical conditions'
            }),
            'disability_details': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Describe any disabilities to help us provide support'
            }),
            'employment_details': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Current employment details'
            }),
            'healthcare_experience_details': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Describe your healthcare experience'
            }),
            'nok_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Next of Kin name'
            }),
            'nok_relationship': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Father, Mother, Sister'
            }),
            'nok_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '08012345678'
            }),
            'nok_address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Next of Kin address'
            }),
        }

    # State of origin choices
    state_of_origin = forms.ChoiceField(
        choices=[
            ('', '-- Select State --'),
            ('Abia', 'Abia'),
            ('Adamawa', 'Adamawa'),
            ('Akwa Ibom', 'Akwa Ibom'),
            ('Anambra', 'Anambra'),
            ('Bauchi', 'Bauchi'),
            ('Bayelsa', 'Bayelsa'),
            ('Benue', 'Benue'),
            ('Borno', 'Borno'),
            ('Cross River', 'Cross River'),
            ('Delta', 'Delta'),
            ('Ebonyi', 'Ebonyi'),
            ('Edo', 'Edo'),
            ('Ekiti', 'Ekiti'),
            ('Enugu', 'Enugu'),
            ('Federal Capital Territory', 'Federal Capital Territory'),
            ('Gombe', 'Gombe'),
            ('Imo', 'Imo'),
            ('Jigawa', 'Jigawa'),
            ('Kaduna', 'Kaduna'),
            ('Kano', 'Kano'),
            ('Katsina', 'Katsina'),
            ('Kebbi', 'Kebbi'),
            ('Kogi', 'Kogi'),
            ('Kwara', 'Kwara'),
            ('Lagos', 'Lagos'),
            ('Nasarawa', 'Nasarawa'),
            ('Niger', 'Niger'),
            ('Ogun', 'Ogun'),
            ('Ondo', 'Ondo'),
            ('Osun', 'Osun'),
            ('Oyo', 'Oyo'),
            ('Plateau', 'Plateau'),
            ('Rivers', 'Rivers'),
            ('Sokoto', 'Sokoto'),
            ('Taraba', 'Taraba'),
            ('Yobe', 'Yobe'),
            ('Zamfara', 'Zamfara'),
        ],
        widget=forms.Select(attrs={'class': 'form-control', 'required': True})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['state_of_origin'].initial = self.instance.state_of_origin


class AcademicHistoryForm(forms.ModelForm):
    """Educational background and examination records"""
    
    class Meta:
        model = AcademicHistory
        fields = [
            'secondary_school_name', 'secondary_school_type', 'secondary_school_state',
            'year_graduated',
            'olevel_sitting_count', 'olevel_exam_type', 'olevel_exam_year',
            'jamb_reg_number', 'jamb_exam_year', 'jamb_score', 'jamb_subject_combination',
            'entry_type',
            'previous_institution', 'previous_program', 'previous_level', 'previous_cgpa',
            'has_olevel_transcript', 'has_jamb_result_slip', 'has_birth_certificate'
        ]
        widgets = {
            'secondary_school_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Name of your secondary school',
                'required': True
            }),
            'secondary_school_type': forms.Select(attrs={'class': 'form-control'}),
            'secondary_school_state': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'State'
            }),
            'year_graduated': forms.NumberInput(attrs={
                'class': 'form-control',
                'type': 'number',
                'min': 1990,
                'max': datetime.now().year,
            }),
            'olevel_sitting_count': forms.RadioSelect(choices=[(1, 'First Sitting'), (2, 'Second Sitting')], attrs={'class': 'form-check-input'}),
            'olevel_exam_type': forms.Select(attrs={'class': 'form-control'}),
            'olevel_exam_year': forms.NumberInput(attrs={
                'class': 'form-control',
                'type': 'number',
                'min': 1990,
                'max': datetime.now().year,
            }),
            'jamb_reg_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'JAMB Registration Number',
                'pattern': '[A-Z0-9]+',
                'title': 'Enter valid JAMB registration number'
            }),
            'jamb_exam_year': forms.NumberInput(attrs={
                'class': 'form-control',
                'type': 'number',
                'min': 2015,
                'max': datetime.now().year,
            }),
            'jamb_score': forms.NumberInput(attrs={
                'class': 'form-control',
                'type': 'number',
                'min': 0,
                'max': 400,
                'placeholder': '0 - 400'
            }),
            'jamb_subject_combination': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Biology, Chemistry, Physics'
            }),
            'entry_type': forms.RadioSelect(choices=[
                ('utme', 'UTME'),
                ('direct_entry', 'Direct Entry'),
                ('transfer', 'Transfer')
            ]),
            'previous_institution': forms.TextInput(attrs={'class': 'form-control'}),
            'previous_program': forms.TextInput(attrs={'class': 'form-control'}),
            'previous_level': forms.TextInput(attrs={'class': 'form-control'}),
            'previous_cgpa': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0.00',
                'max': '5.00'
            }),
        }


class ProgramSelectionForm(forms.Form):
    """Select first and second choice programs"""
    
    PROGRAM_CHOICES = [
        ('', '-- Select Program --'),
        ('pht', 'Public Health Technology'),
        ('himt', 'Health Information Management Technology'),
        ('chew', 'Community Health Extension Workers'),
        ('pt', 'Pharmacy Technician'),
        ('mlt', 'Medical Laboratory Technician'),
    ]
    
    first_choice = forms.ChoiceField(
        choices=PROGRAM_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'required': True
        }),
        label="First Choice Program",
        help_text="Your preferred nursing-related program"
    )
    
    second_choice = forms.ChoiceField(
        choices=PROGRAM_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'required': True
        }),
        label="Second Choice Program",
        help_text="Alternative if first choice is not available"
    )
    
    def clean(self):
        cleaned_data = super().clean()
        first = cleaned_data.get('first_choice')
        second = cleaned_data.get('second_choice')
        
        if first and second and first == second:
            raise forms.ValidationError("First and second choices must be different.")
        
        return cleaned_data


class DocumentUploadForm(forms.ModelForm):
    """Upload supporting documents"""
    
    class Meta:
        model = AdmissionDocument
        fields = ['document_type', 'file']
        widgets = {
            'document_type': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.jpg,.jpeg,.png,.doc,.docx',
                'required': True
            }),
        }
    
    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            # Check file size (max 5MB)
            if file.size > 5 * 1024 * 1024:
                raise forms.ValidationError("File size must not exceed 5MB.")
            
            # Check file type
            allowed_extensions = ['pdf', 'jpg', 'jpeg', 'png', 'doc', 'docx']
            file_ext = file.name.split('.')[-1].lower()
            if file_ext not in allowed_extensions:
                raise forms.ValidationError(f"File type '{file_ext}' not allowed. Use: {', '.join(allowed_extensions)}")
        
        return file


class PaymentForm(forms.Form):
    """Application fee payment form"""
    
    payment_method = forms.ChoiceField(
        choices=[
            ('card', 'Debit Card'),
            ('bank_transfer', 'Bank Transfer'),
            ('ussd', 'USSD'),
        ],
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label="Payment Method"
    )
    
    # For card payments
    cardholder_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Name on card'
        })
    )
    
    card_number = forms.CharField(
        max_length=19,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '1234 5678 9012 3456',
            'pattern': '[0-9]{13,19}'
        })
    )


class ApplicationDecisionForm(forms.ModelForm):
    """Form for registrars to make admission decisions"""
    
    class Meta:
        model = ApplicationRecord
        fields = ['admission_decision', 'admission_notes']
        widgets = {
            'admission_decision': forms.RadioSelect(choices=[
                ('admitted', '✓ Admit'),
                ('rejected', '✗ Reject'),
                ('waitlisted', '⏳ Waitlist'),
            ]),
            'admission_notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Add notes or reasons for this decision...'
            }),
        }
