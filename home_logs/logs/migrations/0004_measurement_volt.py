# -*- coding: utf-8 -*-
# Generated by Django 1.11.24 on 2019-11-16 16:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0003_auto_20190920_1726'),
    ]

    operations = [
        migrations.AddField(
            model_name='measurement',
            name='volt',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True),
        ),
    ]
