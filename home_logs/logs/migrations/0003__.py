# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0003__'),
        ('logs', '0002__'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='measurement',
            unique_together=set([('sensor', 'created_on')]),
        ),
    ]
