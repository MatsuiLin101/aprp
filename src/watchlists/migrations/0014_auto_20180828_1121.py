# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-08-28 03:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('watchlists', '0013_auto_20180814_1602'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='monitorprofile',
            options={'verbose_name': 'Monitor Profile', 'verbose_name_plural': 'Monitor Profile'},
        ),
        migrations.RemoveField(
            model_name='monitorprofile',
            name='comparison',
        ),
        migrations.AddField(
            model_name='monitorprofile',
            name='active',
            field=models.BooleanField(default=False, verbose_name='Period'),
        ),
        migrations.AddField(
            model_name='monitorprofile',
            name='comparator',
            field=models.CharField(choices=[('__lt__', '<'), ('__lte__', '<='), ('__gt__', '>'), ('__gte__', '>=')], default='__lt__', max_length=6, verbose_name='Comparator'),
        ),
        migrations.AlterField(
            model_name='monitorprofile',
            name='color',
            field=models.CharField(choices=[('default', 'Default'), ('info', 'Info'), ('success', 'Success'), ('warning', 'Warning'), ('danger', 'Danger')], default='danger', max_length=20, verbose_name='Color'),
        ),
        migrations.AlterField(
            model_name='monitorprofile',
            name='watchlist',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='watchlists.Watchlist', verbose_name='Watchlist'),
        ),
        migrations.AlterField(
            model_name='watchlistitem',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='watchlists.Watchlist', verbose_name='Parent'),
        ),
    ]
