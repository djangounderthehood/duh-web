from django.test import TestCase


class BasicTestCase(TestCase):
    def test_pages_ok(self):
        """
        Make sure all the pages are accessible.
        """
        for url in ['/', '/coc/', '/accessibility/', '/travel/']:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
