# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendees', '0002_attendee_visible'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendee',
            name='category',
            field=models.CharField(default='regular', max_length=10, choices=[('regular', 'regular'), ('speaker', 'speaker'), ('core', 'core'), ('sponsor', 'sponsor')]),
            preserve_default=True,
        ),
    ]
