# -*- coding: utf-8 -*-

from django.db import models
from django.utils.timezone import localtime


class Notification(models.Model):

    email = models.EmailField()

    viewed = models.BooleanField(default=False)

    sent = models.BooleanField(default=False)


    def mark_as(self, viewed_or_not):
        ''' Mark a notification as viewed or not '''
        self.viewed = viewed_or_not
        self.save()

    def __str__(self):
        return u'Notification for {}'.format(self.email)


class Alert(models.Model):

    space = models.ForeignKey('property.Space')

    sensor = models.ForeignKey('property.Sensor')

    min_value = models.DecimalField(max_digits=6, decimal_places=2,
                                    blank=True)

    max_value = models.DecimalField(max_digits=6, decimal_places=2,
                                    blank=True)

    value = models.DecimalField(max_digits=6, decimal_places=2, blank=True)

    created_on = models.DateTimeField(auto_now_add=True)

    notify = models.ForeignKey(Notification)

    def __str__(self):
        return u'Alert space:{} sensor:{} '.format(self.space.name,
                                                   self.sensor.name)

    def save(self, *args, **kwargs):
        if self.min_value or self.max_value or self.value:
            super(Alert, self).save(*args, **kwargs)
        else:
            raise ValueError('min_value or max_value or value must be set')

