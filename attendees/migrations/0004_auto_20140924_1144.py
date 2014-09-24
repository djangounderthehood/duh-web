# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendees', '0003_attendee_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendee',
            name='visible',
            field=models.BooleanField(default=False),
        ),
    ]
