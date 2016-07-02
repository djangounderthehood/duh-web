from django.db import IntegrityError
from django.shortcuts import resolve_url
from django.test import TestCase

from .forms import ParticipantSignupForm
from .models import TICKET_TYPE_CHOICES, INDIVIDUAL_TICKET, CORPORATE_TICKET, Participant


class ParticipantTest(TestCase):
    def test_email_is_unique(self):
        Participant.objects.create(email='tomek@hauru.eu')

        with self.assertRaises(IntegrityError):
            Participant.objects.create(email='tomek@hauru.eu')


class ParticipantSignupFormTest(TestCase):
    def test_email_is_stripped_and_lowercased(self):
        form = ParticipantSignupForm({
            'first_name': 'Tomek',
            'last_name': 'Paczkowski',
            'email': '   Tomek@Hauru.EU',
            'ticket_type': TICKET_TYPE_CHOICES[0][0]
        })

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['email'], 'tomek@hauru.eu')


class SignupViewTest(TestCase):
    def test_get_renders_form(self):
        resp = self.client.get(resolve_url('signup'))

        self.assertContains(resp, '<form')
        self.assertTemplateUsed(resp, 'lottery/signup.html')

    def test_post_with_incorrect_data_rerenders_form(self):
        resp = self.client.post(resolve_url('signup'), data={})

        self.assertContains(resp, '<form')
        self.assertTemplateUsed(resp, 'lottery/signup.html')

    def test_post_with_correct_data_redirects_to_confirmation(self):
        resp = self.client.post(resolve_url('signup'), data={
            'first_name': 'Tomek',
            'last_name': 'Paczkowski',
            'email': 'tomek@hauru.eu',
            'ticket_type': INDIVIDUAL_TICKET
        })

        self.assertRedirects(resp, resolve_url('signup_confirmation', email='tomek@hauru.eu'))


class SignupConfirmationViewTest(TestCase):
    def test_get_with_incorrect_email_returns_404(self):
        resp = self.client.get(resolve_url('signup_confirmation', email='nope@nope.no'))

        self.assertEqual(404, resp.status_code)

    def test_get_with_correct_email_renders_page(self):
        participant = Participant.objects.create(
            first_name='Tomek', last_name='Paczkowski',
            email='tomek@hauru.eu', ticket_type=CORPORATE_TICKET)
        resp = self.client.get(resolve_url('signup_confirmation', email=participant.email))

        self.assertContains(resp, participant.email)
        self.assertTemplateUsed(resp, 'lottery/signup_confirmation.html')
