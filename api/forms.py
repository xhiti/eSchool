from django import forms
from models import Subject


class SubjectForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Emërtimi i lëndës...',
        'class': 'form-control'
    }))

    description = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Përshkrimi i lëndës...',
        'class': 'form-control'
    }))

    index = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Index-i i lëndës...',
        'class': 'form-control'
    }))

    class Meta:
        model = Subject
        fields = ['title', 'description', 'index']
