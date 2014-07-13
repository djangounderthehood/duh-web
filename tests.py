from django.test import TestCase

from FAQ.models import Entry
from interests.models import Interest


class BasicTestCase(TestCase):
    def test_pages_ok(self):
        """
        Make sure all the pages are accessible.
        """
        for url in ['/', '/FAQ/']:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)


class InterestTestCase(TestCase):
    def test_registration_process(self):
        response = self.client.post('/interest/', data={'email': 'asdf@example.com'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Interest.objects.count(), 1)
        interest = Interest.objects.get()
        self.assertEqual(interest.email, 'asdf@example.com')

    def test_update_process(self):
        interest = Interest.objects.create(email='asdf@example.com')
        response = self.client.post('/interest/%s/' % interest.token, data={'name': 'Baptiste', 'message': 'Hello world!'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Interest.objects.count(), 1)
        interest = Interest.objects.get()
        self.assertEqual(interest.email, 'asdf@example.com')
        self.assertEqual(interest.name, 'Baptiste')
        self.assertEqual(interest.message, 'Hello world!')

    def test_bad_token(self):
        response = self.client.get('/interest/bad_TOKEN/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'interests/token_error.html')

    def test_delete_process(self):
        interest = Interest.objects.create(email='asdf@example.com')
        response = self.client.post('/interest/%s/delete/' % interest.token)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Interest.objects.count(), 0)


class FAQTestCase(TestCase):
    def test_custom_manager(self):
        Entry.objects.create(question='foo', answer='bar')
        self.assertEqual(Entry.objects.published().count(), 0)
        Entry.objects.publish()
        self.assertEqual(Entry.objects.published().count(), 1)
