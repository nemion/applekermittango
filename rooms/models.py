# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db import timezone


# Custom models

class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)
    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value':self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)


# Create your models here.

class Room(models.Model) :
    room_type = models.CharField(max_length=200)
    owner = models.ForeignKey(Person, on_delete = models.cascade)
    nb_guests = models.IntegerRangeField(min_value=1, max_value=10)
    
class Person(models.Model) :
    name = models.CharField(max_length=200)
    date_of_birth = models.DateTimeField()
    
class Reservation(models.Model) :
    guest = models.ForeignKey(Person, on_delete=models.cascade)
    room = models.ForeignKey(Room, on_delete_models.cascade)