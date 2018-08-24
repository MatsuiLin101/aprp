# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-03-31 05:57
from __future__ import unicode_literals

import accounts.utils
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0007_alter_validators_add_error_messages'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AbstractProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=120, verbose_name='Activate Key')),
                ('expired', models.BooleanField(default=False, verbose_name='Expired')),
            ],
            options={
                'verbose_name': 'Abstract Profile',
                'verbose_name_plural': 'Abstract Profiles',
            },
        ),
        migrations.CreateModel(
            name='GroupInformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='Name')),
                ('email_dns', models.CharField(max_length=255, validators=[django.core.validators.URLValidator], verbose_name='Email Dns')),
                ('group', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='info', to='auth.Group', verbose_name='Group')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.GroupInformation', verbose_name='Parent')),
            ],
            options={
                'verbose_name': 'Group Information',
                'verbose_name_plural': 'Group Informations',
            },
        ),
        migrations.CreateModel(
            name='UserInformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_editor', models.BooleanField(default=False, verbose_name='Is Editor')),
                ('profile', models.ImageField(blank=True, null=True, upload_to=accounts.utils.upload_location, verbose_name='Profile')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='info', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'User Information',
                'verbose_name_plural': 'User Informations',
            },
        ),
        migrations.CreateModel(
            name='ActivationProfile',
            fields=[
                ('abstractprofile_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='accounts.AbstractProfile')),
            ],
            options={
                'verbose_name': 'Activation Profile',
                'verbose_name_plural': 'Activation Profiles',
            },
            bases=('accounts.abstractprofile',),
        ),
        migrations.CreateModel(
            name='ResetEmailProfile',
            fields=[
                ('abstractprofile_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='accounts.AbstractProfile')),
                ('new_email', models.EmailField(max_length=254, verbose_name='Reset Email')),
            ],
            options={
                'verbose_name': 'Reset Email Profile',
                'verbose_name_plural': 'Reset Email Profiles',
            },
            bases=('accounts.abstractprofile',),
        ),
        migrations.CreateModel(
            name='ResetPasswordProfile',
            fields=[
                ('abstractprofile_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='accounts.AbstractProfile')),
            ],
            options={
                'verbose_name': 'Reset Password Profile',
                'verbose_name_plural': 'Reset Password Profiles',
            },
            bases=('accounts.abstractprofile',),
        ),
        migrations.AddField(
            model_name='abstractprofile',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
    ]
