from django.test import TestCase

from FAQ.models import Entry


class BasicTestCase(TestCase):
    def test_pages_ok(self):
        """
        Make sure all the pages are accessible.
        """
        for url in ['/', '/FAQ/']:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)


class FAQTestCase(TestCase):
    def test_custom_manager(self):
        Entry.objects.create(question='foo', answer='bar')
        self.assertEqual(Entry.objects.published().count(), 0)
        Entry.objects.publish()
        self.assertEqual(Entry.objects.published().count(), 1)
