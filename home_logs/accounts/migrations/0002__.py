# -*- coding: utf-8 -*-
# Generated by Django 1.11.24 on 2019-09-26 13:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='allow_panel',
            field=models.BooleanField(default=False, help_text=b'Allow user to login in custom panel'),
        ),
    ]
