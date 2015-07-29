# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendees', '0004_auto_20140924_1144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendee',
            name='category',
            field=models.CharField(choices=[('regular', 'regular'), ('speaker', 'speaker'), ('core', 'core'), ('sponsor', 'sponsor'), ('test', 'test')], max_length=10, default='regular'),
        ),
    ]
