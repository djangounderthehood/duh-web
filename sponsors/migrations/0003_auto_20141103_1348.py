# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sponsors', '0002_auto_20140917_2017'),
    ]

    operations = [
        migrations.AddField(
            model_name='sponsor',
            name='is_live',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sponsor',
            name='description',
            field=models.TextField(help_text="Use `[[link text]]` to create a link to the sponsor's URL.", blank=True),
        ),
    ]
