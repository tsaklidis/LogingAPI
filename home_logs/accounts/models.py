#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):

    allow_tokens = models.BooleanField(
        default=True, help_text="Allow user to ask tokens")

    unlimited_tokens = models.BooleanField(
        default=False, help_text="Allow creating unlimited tokens")
    persistent_tokens = models.BooleanField(
        default=False, help_text="Allow creating persistent tokens")

    allow_panel = models.BooleanField(
        default=False, help_text="Allow user to login in custom panel")

    def __unicode__(self):
        return u'CustomUser: {}'.format(self.username)
