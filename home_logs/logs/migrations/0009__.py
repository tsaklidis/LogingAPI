# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0007__'),
        ('logs', '0008_auto_20260307_1449'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='measurement',
            index=models.Index(fields=['space', 'created_on'], name='logs_measur_space_i_a1b2c3_idx'),
        ),
        migrations.AddIndex(
            model_name='measurement',
            index=models.Index(fields=['space', 'sensor'], name='logs_measur_space_i_d4e5f6_idx'),
        ),
        migrations.AddIndex(
            model_name='measurement',
            index=models.Index(fields=['created_on'], name='logs_measur_created_7g8h9i_idx'),
        ),
        migrations.AddIndex(
            model_name='measurement',
            index=models.Index(fields=['space', 'sensor', 'created_on'], name='logs_measur_space_s_j1k2l3_idx'),
        ),
        migrations.AddIndex(
            model_name='measurement',
            index=models.Index(fields=['space', 'sensor', '-created_on'], name='logs_measur_space_s_m4n5o6_idx'),
        ),
    ]

