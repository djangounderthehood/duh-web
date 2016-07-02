from unittest.mock import patch

from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import resolve_url
from django.test import TestCase
from django.utils import timezone

from .forms import ParticipantSignupForm
from .models import TICKET_TYPE_CHOICES, INDIVIDUAL_TICKET, CORPORATE_TICKET, Participant, Batch


class BatchTest(TestCase):
    participants_created = 0

    def test_assigned_is_false_when_not_assigned(self):
        batch = Batch()

        self.assertFalse(batch.assigned)

    def test_assigned_is_true_when_assigned(self):
        batch = Batch(assigned_at=timezone.now())

        self.assertTrue(batch.assigned)

    def test_assign_participants_fails_on_already_assigned(self):
        batch = Batch(assigned_at=timezone.now())

        with self.assertRaises(ValueError):
            batch.assign_participants()

    def test_assign_participants_does_assign_participants(self):
        participants = [self.create_participant() for n in range(5)]
        batch = Batch.objects.create(name='Test Batch', tickets=3)
        batch.assign_participants()

        self.assertTrue(batch.assigned)
        self.assertEqual(3, batch.participants.count())
        self.assertEqual(2, Participant.objects.filter(batch=None).count())

    def create_participant(self):
        self.participants_created += 1
        return Participant.objects.create(
            first_name='Alice',
            last_name='Doe',
            email='alice-%s@example.com' % self.participants_created,
            ticket_type=INDIVIDUAL_TICKET,
        )


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


class BatchAdminTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser('admin', 'admin@example.com', 'admin')
        self.client.login(username='admin', password='admin')

    def test_assign_participants_action_works(self):
        batch = Batch.objects.create(name='Test Batch', tickets=50)
        change_url = resolve_url('admin:lottery_batch_changelist')

        with patch.object(Batch, 'assign_participants') as assign_participants_mock:
            assign_participants_mock.return_value = 50
            resp = self.client.post(change_url, follow=True, data={
                'action': 'assign_participants',
                '_selected_action': '%d' % batch.pk
            }, )

            assign_participants_mock.assert_called_once_with()
            self.assertEqual(1, len(resp.context['messages']))
