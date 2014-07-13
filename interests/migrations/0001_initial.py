# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Interest',
            fields=[
                ('email', models.EmailField(primary_key=True, serialize=False, max_length=75, verbose_name='email')),
                ('name', models.CharField(blank=True, max_length=200, verbose_name='name')),
                ('message', models.TextField(blank=True, verbose_name='message')),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='created on')),
            ],
            options={
                'verbose_name_plural': 'interests',
                'verbose_name': 'interest',
            },
            bases=(models.Model,),
        ),
    ]
