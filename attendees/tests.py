from django.test import TestCase

from .models import Attendee


class AttendeeTestCase(TestCase):
    def test_email_private(self):
        """
        Make sure we don't leak email addresses in avatar URL.
        """
        a = Attendee(reference='asdf', name='Batistek', email='batistek@gmail.pl')
        avatar_URL = a.avatar
        self.assertNotIn('batistek', a.avatar)
