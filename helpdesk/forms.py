from django import forms
from .models import InternalEnquiry, ExternalEnquiry



class InternalEnquiryForm(forms.ModelForm):
    class Meta:
        model = InternalEnquiry
        fields = ('title', 'technical_issue', 'message')
        exclude = ('user_detail',)
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enquiry Title'}),
            'technical_issue': forms.TextInput(attrs={'placeholder': 'Technical Description'}),
            'message': forms.Textarea(attrs={'placeholder': 'Message'})
    }


class ExternalEnquiryForm(forms.ModelForm):
    class Meta:
        model = ExternalEnquiry
        fields = ('name_surname', 'email', 'phone', 'title', 'technical_issue', 'message')
        exclude = ('user_detail',)
        widgets = {
            'name_surname': forms.TextInput(attrs={'placeholder': 'Your Name & Surname'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Your e-Mail Address'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Your Phone Number'}),
            'title': forms.TextInput(attrs={'placeholder': 'Enquiry Title'}),
            'technical_issue': forms.TextInput(attrs={'placeholder': 'Technical Description'}),
            'message': forms.Textarea(attrs={'placeholder': 'Message'})
    }