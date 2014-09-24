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

    def test_twitter_cleanup(self):
        for twitter in ['@batistek', 'batistek', 'twitter.com/batistek']:
            a = Attendee.objects.create(reference='asdf', name='Batistek', email='batistek@gmail.pl', twitter=twitter)
            self.assertEqual(a.twitter, 'batistek')

    def test_twitter_cleanup_None(self):
        """
        Make sure that using '-' as a twitter name is saved as None.
        """
        a = Attendee.objects.create(reference='asdf', name='Batistek', email='batistek@gmail.pl', twitter='-')
        self.assertIs(a.twitter, None)
