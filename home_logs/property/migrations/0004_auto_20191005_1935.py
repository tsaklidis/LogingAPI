# -*- coding: utf-8 -*-
# Generated by Django 1.11.24 on 2019-10-05 16:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0003__'),
    ]

    operations = [
        migrations.AlterField(
            model_name='house',
            name='spaces',
            field=models.ManyToManyField(blank=True, related_name='space', to='property.Space'),
        ),
    ]
