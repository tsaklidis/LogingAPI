# -*- coding: utf-8 -*-
# Generated by Django 1.11.24 on 2019-09-05 12:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('property', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Measurement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.DecimalField(decimal_places=2, max_digits=6)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('sensor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='measurements', to='property.Sensor')),
            ],
        ),
    ]
