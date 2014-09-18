import re

from django.db import models
from django.utils.html import format_html
from django.utils import timezone


class SPONSOR_LEVELS:
    GOLD = 'gold'
    SILVER = 'silver'
    PARTNER = 'partner'

    choices = [
        (GOLD, 'Gold'),
        (SILVER, 'Silver'),
        (PARTNER, 'Partner')
    ]


class SponsorQueryset(models.QuerySet):
    def gold(self):
        return self._by_level(SPONSOR_LEVELS.GOLD)

    def silver(self):
        return self._by_level(SPONSOR_LEVELS.SILVER)

    def partner(self):
        return self._by_level(SPONSOR_LEVELS.PARTNER)

    def _by_level(self, level):
        return self.filter(level=level).order_by('?')


class Sponsor(models.Model):
    LEVELS = SPONSOR_LEVELS

    level = models.CharField(max_length=20, choices=LEVELS.choices)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, help_text="Use `[[link text]]` to create a link to the sponsor's URL.")
    logo = models.ImageField(blank=True)
    url = models.URLField(blank=True)
    created_on = models.DateTimeField(default=timezone.now, editable=False)

    objects = SponsorQueryset.as_manager()

    def __str__(self):
        return self.name

    @property
    def linkified_description(self):
        """
        Replaces [[foo]] with <a href="{{ self.url }}">foo</a>.
        """
        links = []
        def linkify(matchobj, links=links):
            link = format_html('<a href="{0}" target="_blank">{1}</a>', self.url, matchobj.group(1))
            links.append(link)
            return '{%d}' % (len(links) - 1)

        fmt = re.sub(r'\[\[([^\]]+)\]\]', linkify, self.description)
        return format_html(fmt, *links)
