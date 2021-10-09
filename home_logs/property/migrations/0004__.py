# -*- coding: utf-8 -*-
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
