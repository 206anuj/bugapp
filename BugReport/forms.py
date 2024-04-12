from django import forms
from .models import Bug

class ReportForm(forms.ModelForm):
    class Meta:
        model = Bug
        fields = ['project', 'SDM', 'issue_reported', 'resolved_by',]