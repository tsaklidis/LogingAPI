# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations

from home_logs.utils.unique import get


def generate_kinds(apps, schema_editor):

    SpaceKind = apps.get_model('property', 'SpaceKind')
    SensorKind = apps.get_model('property', 'SensorKind')
    Sensor = apps.get_model('property', 'Sensor')

    kinds = [
        'Storage', 'Classroom', 'Safe',
        'Secret', 'Basement', 'Garage',
        'Cellar', 'Livingroom', 'Kitchen',
        'Bathroom', 'Bedroom'
    ]

    sensor_kinds = ['temperature', 'humidity', 'presure', 'light', 'timer']
    sensors = {
        'LM35': 'temperature',
        'DS18B20': 'temperature',
        'DHT22': 'humidity',
        'DHT22': 'temperature',
        'Clock': 'timer',
    }

    for kind in kinds:
        SpaceKind.objects.create(name=kind)

    for skind in sensor_kinds:
        SensorKind.objects.create(name=skind)

    for name, s_kind in sensors.items():
        kind = SensorKind.objects.get(name=s_kind)
        Sensor.objects.create(name=name, kind=kind, uuid=get(5))


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0002__'),
    ]

    operations = [
        migrations.RunPython(generate_kinds),
    ]
