#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils.translation import ugettext_lazy as _

from home_logs.utils.unique import get

from home_logs.logs.models import Measurement


class House(models.Model):

    name = models.CharField(max_length=50, default='MyHome',
                            null=False, blank=False)

    created_on = models.DateTimeField(auto_now_add=True)

    uuid = models.CharField(unique=True, max_length=50,
                            default=get, editable=False)

    spaces = models.ManyToManyField(
        'property.Space', blank=True, related_name='space')

    owner = models.ForeignKey(get_user_model(), null=True)

    @property
    def sensors_count(self):
        sensors = 0
        for space in self.spaces.all():
            sensors = sensors + space.sensors_count
        return sensors

    @property
    def sensors_objs(self):
        sensors = []
        for space in self.spaces.all():
            for sensor in space.sensors.all():
                if sensor not in sensors:
                    sensors.append(sensor)
        return sensors

    @property
    def spaces_count(self):
        return self.spaces.count()

    def __str__(self):
        return u'House: {}'.format(self.name)


class Space(models.Model):

    name = models.CharField(max_length=50, default='MyRoom',
                            null=False, blank=False)

    kind = models.ForeignKey('property.SpaceKind', null=False, blank=False)

    sensors = models.ManyToManyField('property.Sensor', related_name='spaces',
                                                                     blank=True)
    owner = models.ForeignKey(get_user_model(), null=True)

    uuid = models.CharField(unique=True, max_length=50,
                            default=get, editable=False)

    created_on = models.DateTimeField(auto_now_add=True)

    x_length = models.DecimalField(max_digits=6, decimal_places=2, default=0,
                                   help_text='Using meters')

    y_length = models.DecimalField(max_digits=6, decimal_places=2, default=0,
                                   help_text='Using meters')

    @property
    def square_meters(self):
        return round((abs(self.x_length) * abs(self.y_length)), 2)

    @property
    def sensors_count(self):
        return self.sensors.count()

    @property
    def house(self):
        try:
            return House.objects.get(spaces__id=self.id)
        except ObjectDoesNotExist:
            return 'This House'

    def __str__(self):
        # Creating space from house. Inside admin django panel
        try:
            return u'{} @ {}'.format(self.name, self.house.name)
        except AttributeError:
            return u'{} @ {}'.format(self.name, self.house)


class Sensor(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)

    location = models.CharField(max_length=50, null=True, blank=True)

    kind = models.ForeignKey('property.SensorKind', null=False, blank=False)

    uuid = models.CharField(unique=True, max_length=50,
                            default=get, editable=False)

    def get_values(self):
        ms = Measurement.objects.filter(sensor=self)
        return ms

    def __str__(self):
        return u'{}'.format(self.name)


class SensorKind(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return u'{}'.format(self.name)


class SpaceKind(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return u'{}'.format(self.name)
