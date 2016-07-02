from django import forms

from .models import Participant


class ParticipantSignupForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['first_name', 'last_name', 'email', 'ticket_type']

    def clean_email(self):
        email = self.cleaned_data['email']
        return email.strip().lower()
