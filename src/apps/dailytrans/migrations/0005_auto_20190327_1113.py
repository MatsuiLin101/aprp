# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2019-03-27 03:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dailytrans', '0004_dailytran_create_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailytran',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Create Time'),
        ),
    ]
