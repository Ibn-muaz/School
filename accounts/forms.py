"""
Forms for student biodata and profile completion.
"""

from django import forms
from accounts.models import StudentProfile, User


class StudentBioDataForm(forms.ModelForm):
    """
    Form for students to complete their biodata after first login.
    This is required before they can access full portal features.
    """
    
    # User fields (in User model)
    first_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First Name'
        })
    )
    
    last_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last Name'
        })
    )
    
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email Address'
        })
    )
    
    phone_number = forms.CharField(
        max_length=17,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Phone Number (e.g., +234801234567)'
        })
    )
    
    # StudentProfile fields
    class Meta:
        model = StudentProfile
        fields = [
            'matriculation_number',  # Read-only, display only
            'department',
            'level',
            'nationality',
            'state_of_origin',
            'local_government',
        ]
        widgets = {
            'matriculation_number': forms.TextInput(attrs={
                'class': 'form-control',
                'readonly': 'readonly',
                'disabled': 'disabled',
            }),
            'department': forms.TextInput(attrs={
                'class': 'form-control',
                'readonly': 'readonly',
                'disabled': 'disabled',
            }),
            'level': forms.TextInput(attrs={
                'class': 'form-control',
                'readonly': 'readonly',
                'disabled': 'disabled',
            }),
            'nationality': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nationality'
            }),
            'state_of_origin': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'State of Origin'
            }),
            'local_government': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Local Government Area'
            }),
        }
    
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Pre-fill user fields from User model
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email
            self.fields['phone_number'].initial = user.phone_number
    
    def save(self, commit=True):
        """Save both StudentProfile and linked User instance."""
        instance = super().save(commit=False)
        
        # Get the user from the profile
        user = instance.user
        
        # Update user fields
        user.first_name = self.cleaned_data.get('first_name', '')
        user.last_name = self.cleaned_data.get('last_name', '')
        user.email = self.cleaned_data.get('email', '')
        user.phone_number = self.cleaned_data.get('phone_number', '')
        
        if commit:
            user.save()
            instance.profile_completed = True  # Mark profile as completed
            instance.save()
        
        return instance


class ChangePasswordForm(forms.Form):
    """Form for students to change their default password."""
    
    old_password = forms.CharField(
        label='Current Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter current password'
        })
    )
    
    new_password = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter new password'
        }),
        min_length=8
    )
    
    confirm_password = forms.CharField(
        label='Confirm New Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm new password'
        })
    )
    
    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if new_password and confirm_password:
            if new_password != confirm_password:
                raise forms.ValidationError("New passwords do not match.")
        
        return cleaned_data
