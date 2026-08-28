from django import forms
from .models import QuoteRequest


class QuoteRequestForm(forms.ModelForm):
    class Meta:
        model = QuoteRequest
        fields = [
            'full_name', 'email', 'phone', 'address',
            'service', 'is_emergency', 'message',
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Full name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control', 'placeholder': 'you@example.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': '07700 900 123'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Address, including postcode'
            }),
            'service': forms.Select(attrs={'class': 'form-select'}),
            'is_emergency': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'message': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 5,
                'placeholder': "Tell us what's going on and we'll get back to you quickly."
            }),
        }
        labels = {
            'is_emergency': 'This is an emergency (burst pipe, no heating, leak, etc.)',
        }


class AdminReplyForm(forms.ModelForm):
    """Used on the private staff dashboard to update a job's status and
    write a reply back to the customer (sent by email)."""

    class Meta:
        model = QuoteRequest
        fields = ['status', 'admin_reply']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'admin_reply': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 6,
                'placeholder': "Write a reply to send to the customer by email (optional)...",
            }),
        }
        labels = {
            'admin_reply': 'Reply to customer',
        }
