# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-10-23 07:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0008_auto_20181016_1609'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='content_type',
            field=models.ForeignKey(default=26, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType'),
        ),
    ]
