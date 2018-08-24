# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-03-31 05:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('configs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fruit',
            fields=[
                ('abstractproduct_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='configs.AbstractProduct')),
            ],
            options={
                'verbose_name': 'Fruit',
                'verbose_name_plural': 'Fruits',
            },
            bases=('configs.abstractproduct',),
        ),
    ]
