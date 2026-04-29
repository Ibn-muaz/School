"""
Clearance forms — document uploads, acceptance fee, and approval forms.
"""

from django import forms
from .models import ClearanceDocument, StudentClearance


class ClearanceDocumentUploadForm(forms.ModelForm):
    """Form for students to upload clearance documents."""
    class Meta:
        model = ClearanceDocument
        fields = ['document_type', 'file']
        widgets = {
            'document_type': forms.Select(attrs={
                'class': 'form-control',
                'id': 'id_document_type',
            }),
            'file': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.jpg,.jpeg,.png',
                'id': 'id_file',
            }),
        }

    def clean_file(self):
        f = self.cleaned_data.get('file')
        if f:
            # Max 5 MB
            if f.size > 5 * 1024 * 1024:
                raise forms.ValidationError("File size must not exceed 5 MB.")
            # Allowed extensions
            ext = f.name.rsplit('.', 1)[-1].lower()
            if ext not in ('pdf', 'jpg', 'jpeg', 'png'):
                raise forms.ValidationError("Only PDF, JPG, JPEG, and PNG files are allowed.")
        return f


class AcceptanceFeeForm(forms.Form):
    """Simulated acceptance fee payment form."""
    payment_method = forms.ChoiceField(
        choices=[
            ('online', 'Online Payment'),
            ('bank_transfer', 'Bank Transfer'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    confirm = forms.BooleanField(
        required=True,
        label="I confirm this payment",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    )


class ClearanceApprovalForm(forms.Form):
    """Form for registrar to approve/reject clearance."""
    decision = forms.ChoiceField(
        choices=[('approve', 'Approve Clearance'), ('reject', 'Reject Clearance')],
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Optional notes or rejection reason...',
        }),
    )


class AcceptanceFeeConfigForm(forms.ModelForm):
    """Form for bursary to update acceptance fee amount."""
    class Meta:
        model = StudentClearance
        fields = ['acceptance_fee_amount']
        widgets = {
            'acceptance_fee_amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
            }),
        }
