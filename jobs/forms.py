from django import forms
from .models import Job, Application

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        exclude = ('recruiter',)
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'requirements': forms.Textarea(attrs={'rows': 4}),
        }

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ('resume_link', 'cover_letter')
        widgets = {
            'cover_letter': forms.Textarea(attrs={'rows': 4}),
        }
