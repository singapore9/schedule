# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-25 19:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('custom_auth', '0005_auto_20170425_1905'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='token',
            name='user',
        ),
        migrations.RemoveField(
            model_name='applicationuser',
            name='last_login',
        ),
        migrations.RemoveField(
            model_name='applicationuser',
            name='password',
        ),
        migrations.RemoveField(
            model_name='applicationuser',
            name='username',
        ),
        migrations.DeleteModel(
            name='Token',
        ),
    ]
