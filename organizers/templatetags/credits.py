from __future__ import unicode_literals
from random import shuffle

from django import template

register = template.Library()

@register.simple_tag
def organizers():
    authors = [
        'Baptiste Mispelon',
        'Erik Romijn',
        'Ola Sitarska',
        'Marc Tamlyn',
        'Ola Sendecka',
        'Tomek Paczkowski',
    ]
    shuffle(authors)
    return '%s, and %s' % (
        ', '.join(authors[:-1]),
        authors[-1]
    )
