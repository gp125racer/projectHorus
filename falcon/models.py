from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

import time


class Device(models.Model):
    type_choices = (
        ('100', 'Multi-Rotor'),
        ('200', 'Aircraft'),
        ('300', 'Ground')
    )

    model_choices = (
        ('100', 'Alpha'),
        ('200', 'Beta'),
        ('300', 'v1'),
        ('400', 'v2')
    )

    creator = models.ForeignKey(User, blank=False)
    name = models.CharField(max_length=200, blank=False)
    uid = models.UUIDField(blank=True)
    registered = models.BooleanField(default=False, blank=True)
    created_at = models.DateTimeField(default=time.time(), blank=True)
    modified_at = models.DateTimeField(default=time.time(), blank=True)
    type = models.CharField(max_length=100, blank=False, choices=type_choices)
    model =models.CharField(max_length=100, blank=False, choices=model_choices)

    def __unicode__(self):
        return self.name


class FlightPlan(models.Model):
    creator = models.ForeignKey(User, blank=False)
    name = models.CharField(max_length=200, blank=False)
    uid = models.UUIDField(blank=True)
    data = models.CharField(max_length=2000, blank=True)
    created_at = models.DateTimeField(default=time.time(), blank=True)
    modified_at = models.DateTimeField(default=time.time(), blank=True)

    def as_dict(self):
        return {
            "creator":self.creator.username,
            "name":self.name,
            "data":self.data,
            "uid":self.uid.hex,
        }

    def __unicode__(self):
        return self.name


class Mission(models.Model):
    creator = models.ForeignKey(User, blank=False)
    name = models.CharField(max_length=200, blank=False)
    uid = models.UUIDField(blank=True)
    flight_plan = models.ForeignKey(FlightPlan, blank=False)
    device = models.ForeignKey(Device, blank=False)
    start_time = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(default=False, blank=True)
    completed = models.BooleanField(default=False, blank=True)
    created_at = models.DateTimeField(default=time.time(), blank=True)
    modified_at = models.DateTimeField(default=time.time(), blank=True)

    def as_dict(self):
        return {
            "creator": self.creator.username,
            "name": self.name,
            "uid": self.uid.hex,
            "flight_plan": self.flight_plan.as_dict(),
            "device": self.device.name,
            "start_time": self.start_time,
            "active": self.active,
            "completed": self.completed,
            "created_at": self.created_at,
            "modified_at": self.modified_at
        }

    def __unicode__(self):
        return self.name