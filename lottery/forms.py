import html2text
from django import forms
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from .models import Participant


class ParticipantSignupForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['first_name', 'last_name', 'email', 'ticket_type']

    def clean_email(self):
        email = self.cleaned_data['email']
        return email.strip().lower()
        
    def save(self):
        participant = super(ParticipantSignupForm, self).save()
        if participant:
            html_message = render_to_string('lottery/email_confirmation.html')
            message = html2text.html2text(html_message)
            send_mail(
                subject="Django: Under The Hood 2016 ticket lottery confirmation",
                message=message,
                from_email=settings.SERVER_EMAIL,
                recipient_list=[participant.email],
                fail_silently=True,
                html_message=html_message
            )
        return participant
