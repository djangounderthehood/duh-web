from django.db import models

from django_gravatar.helpers import get_gravatar_url


class Attendee(models.Model):
    reference = models.CharField(max_length=6, null=False, blank=False)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    twitter = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def avatar(self):
        default = 'http://api.adorable.io/avatar/100/%s.png' % (self.email)
        return get_gravatar_url(self.email.lower(), default=default)
