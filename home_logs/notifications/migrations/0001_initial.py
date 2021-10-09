# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('property', '0005__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Alert',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('min_value', models.DecimalField(blank=True, decimal_places=2, max_digits=6)),
                ('max_value', models.DecimalField(blank=True, decimal_places=2, max_digits=6)),
                ('value', models.DecimalField(blank=True, decimal_places=2, max_digits=6)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('viewed', models.BooleanField(default=False)),
                ('sent', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='alert',
            name='notify',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='notifications.Notification'),
        ),
        migrations.AddField(
            model_name='alert',
            name='sensor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='property.Sensor'),
        ),
        migrations.AddField(
            model_name='alert',
            name='space',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='property.Space'),
        ),
    ]
