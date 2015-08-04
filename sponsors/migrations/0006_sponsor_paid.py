# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sponsors', '0005_auto_20150804_1005'),
    ]

    operations = [
        migrations.AddField(
            model_name='sponsor',
            name='paid',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
