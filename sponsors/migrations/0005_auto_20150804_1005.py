# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sponsors', '0004_auto_20150729_1952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sponsor',
            name='is_live',
            field=models.BooleanField(default=False),
        ),
    ]
