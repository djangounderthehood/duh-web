# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sponsor',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('level', models.CharField(choices=[('gold', 'Gold'), ('silver', 'Silver'), ('partner', 'Partner')], max_length=20)),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('logo', models.ImageField(upload_to='')),
                ('url', models.URLField(blank=True)),
                ('created_on', models.DateTimeField(editable=False, default=django.utils.timezone.now)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
