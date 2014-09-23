# -*- coding: utf-8 -*-
import hashlib, urllib

from django.db import models

class Attendee(models.Model):
    reference = models.CharField(max_length=6, null=False, blank=False)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    twitter = models.CharField(max_length=100, null=True, blank=True)

    def __unicode__(self):
        return self.name

    def avatar(self):
        default = 'http://api.adorable.io/avatar/100/%s.png' % (self.email)
        gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(self.email.lower()).hexdigest() + "?"
        gravatar_url += urllib.urlencode({'d':default, 's':'100'})

        return gravatar_url
