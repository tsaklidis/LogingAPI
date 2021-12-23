#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.utils.timezone import localtime


class Measurement(models.Model):
    space = models.ForeignKey('property.Space', null=True)

    sensor = models.ForeignKey(
        'property.Sensor', null=False, related_name='measurements')

    value = models.DecimalField(max_digits=6, decimal_places=2, blank=False)

    created_on = models.DateTimeField(auto_now_add=True)

    custom_created_on = models.DateTimeField(null=True, blank=True)

    volt = models.DecimalField(max_digits=6, decimal_places=2,
                               blank=True, null=True)

    def __str__(self):
        return u'For {}'.format(self.sensor)

    @property
    def created_localtime(self):
        # Convert time to settings.timezone zone
        # created on is saved on utc
        return localtime(self.created_on)

    class Meta:
        # ensure user and name are unique
        unique_together = ('sensor', 'created_on',)


class DavisMeasurement(models.Model):
    value = models.DecimalField(max_digits=6, decimal_places=2, blank=False)

    kind = models.CharField(max_length=50, null=False, blank=False)

    measured = models.DateTimeField()

    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return u'{}: {}'.format(self.kind, self.value)

    class Meta:
        # Avoid duplicates
        unique_together = ('measured', 'kind',)