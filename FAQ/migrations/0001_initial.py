# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('question', models.TextField(help_text='You can use HTML.', verbose_name='question')),
                ('answer', models.TextField(help_text='You can use HTML.', verbose_name='answer')),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='created on')),
                ('published', models.BooleanField(default=False, verbose_name='published')),
            ],
            options={
                'verbose_name_plural': 'entries',
                'verbose_name': 'entry',
            },
            bases=(models.Model,),
        ),
    ]
