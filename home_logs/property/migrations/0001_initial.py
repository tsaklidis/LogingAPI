# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import home_logs.utils.unique


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='House',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=b'MyHome', max_length=50)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('uuid', models.CharField(default=home_logs.utils.unique.get, editable=False, max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('location', models.CharField(max_length=50, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='SensorKind',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Space',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=b'MyRoom', max_length=50)),
                ('uuid', models.CharField(default=home_logs.utils.unique.get, editable=False, max_length=50, unique=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('x_length', models.DecimalField(decimal_places=2, default=0, help_text=b'Using meters', max_digits=6)),
                ('y_length', models.DecimalField(decimal_places=2, default=0, help_text=b'Using meters', max_digits=6)),
            ],
        ),
        migrations.CreateModel(
            name='SpaceKind',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='space',
            name='kind',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='property.SpaceKind'),
        ),
        migrations.AddField(
            model_name='space',
            name='sensors',
            field=models.ManyToManyField(blank=True, related_name='spaces', to='property.Sensor'),
        ),
        migrations.AddField(
            model_name='sensor',
            name='kind',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='property.SensorKind'),
        ),
        migrations.AddField(
            model_name='house',
            name='spaces',
            field=models.ManyToManyField(blank=True, to='property.Space'),
        ),
    ]
