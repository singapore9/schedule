# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-25 19:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduleapp', '0002_auto_20170424_1054'),
        ('custom_auth', '0003_auto_20170409_1210'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicationuser',
            name='unvisited_lessons',
            field=models.ManyToManyField(related_name='slackers', to='scheduleapp.Lesson'),
        ),
        migrations.AddField(
            model_name='applicationuser',
            name='visited_lessons',
            field=models.ManyToManyField(related_name='visitors', to='scheduleapp.Lesson'),
        ),
    ]
