# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-07-05 14:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configs', '0004_auto_20180705_2212'),
    ]

    operations = [
        migrations.AddField(
            model_name='chart',
            name='template_name',
            field=models.CharField(default='', max_length=255, verbose_name='Template Name'),
            preserve_default=False,
        ),
    ]
