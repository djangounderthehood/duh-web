from django import forms

from .models import Interest


class RegisterInterestForm(forms.ModelForm):
    class Meta:
        model = Interest
        fields = ['email']


class UpdateInterestForm(forms.ModelForm):
    class Meta:
        model = Interest
        fields = ['name', 'message']
