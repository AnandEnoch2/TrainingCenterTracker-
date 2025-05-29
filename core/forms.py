from django import forms
from .models import EmployeeTask

class EmployeeTaskForm(forms.ModelForm):
    class Meta:
        model = EmployeeTask
        fields = ['user','task_desc', 'status']



from django import forms
from .models import Admission

class AdmissionForm(forms.ModelForm):
    class Meta:
        model = Admission
        fields = ['student', 'course', 'amount_paid']
        widgets = {
            'amount_paid': forms.NumberInput(attrs={'class': 'form-control'}),
            'student': forms.Select(attrs={'class': 'form-control'}),
            'course': forms.Select(attrs={'class': 'form-control'}),
        }



from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']


from django import forms
from .models import DailyReport  # Make sure this matches your model

class DailyReportForm(forms.ModelForm):
    class Meta:
        model = DailyReport
        fields = ['batch', 'topic_covered', 'students_present']
        widgets = {
            'batch': forms.TextInput(attrs={
                'placeholder': 'Enter batch name or ID',
                'class': 'form-control',
            }),
            'topic_covered': forms.TextInput(attrs={
                'placeholder': 'Enter the topics covered today',
                'class': 'form-control',
            }),
            'students_present': forms.CheckboxSelectMultiple(attrs={
                'class': 'checkbox-group',
            }),
        }
