from django.test import TestCase

from .models import Sponsor

class SponsorTestCase(TestCase):
    def test_linkified(self):
        sponsor = Sponsor(
            name='foo',
            level=Sponsor.LEVELS.GOLD,
            url="http://example.com",
            description="[[foo]]"
        )
        self.assertHTMLEqual(sponsor.linkified_description, '<a href="http://example.com" target="_blank">foo</a>')
