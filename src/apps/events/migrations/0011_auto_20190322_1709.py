# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2019-03-22 09:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0010_auto_20190108_1332'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='content_type',
            field=models.ForeignKey(default=23, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType'),
        ),
    ]
