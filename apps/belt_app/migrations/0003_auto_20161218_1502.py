# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-18 23:02
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('belt_app', '0002_user_birthday'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='first_name',
            new_name='alias',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='last_name',
            new_name='name',
        ),
    ]
