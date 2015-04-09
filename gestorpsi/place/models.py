# -*- coding: utf-8 -*-

"""
Copyright (C) 2008 GestorPsi

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""

import reversion
from datetime import datetime
from django.db import models
from gestorpsi.address.models import Address
from gestorpsi.phone.models import Phone
from django.contrib.contenttypes import generic
from gestorpsi.organization.models import Organization
from gestorpsi.util.uuid_field import UuidField


class PlaceType(models.Model):
    """
    This class represents place types.
    @version: 1.0
    """
    description = models.CharField(max_length=100)

    def __unicode__(self):
        return "%s" % self.description

    class Meta:
        ordering = ['description']


class PlaceManager(models.Manager):
    def active(self):
        return super(PlaceManager, self).get_query_set().filter(active=True)

    def deactive(self):
        return super(PlaceManager, self).get_query_set().filter(active=False)

HOURS = (
        ('00:00', '00,00'),
        ('00:30', '00,30'),
        ('01:00', '01,00'),
        ('01:30', '01,30'),
        ('02:00', '02,00'),
        ('02:30', '02,30'),
        ('03:00', '03,00'),
        ('03:30', '03,30'),
        ('04:00', '04,00'),
        ('04:30', '04,30'),
        ('05:00', '05,00'),
        ('05:30', '05,30'),
        ('06:00', '06,00'),
        ('06:30', '06,30'),
        ('07:00', '07,00'),
        ('07:30', '07,30'),
        ('08:00', '08,00'),
        ('08:30', '08,30'),
        ('09:00', '09,00'),
        ('09:30', '09,30'),
        ('10:00', '10,00'),
        ('10:30', '10,30'),
        ('11:00', '11,00'),
        ('11:30', '11,30'),
        ('12:00', '12,00'),
        ('12:30', '12,30'),
        ('13:00', '13,00'),
        ('13:30', '13,30'),
        ('14:00', '14,00'),
        ('14:30', '14,30'),
        ('15:00', '15,00'),
        ('15:30', '15,30'),
        ('16:00', '16,00'),
        ('16:30', '16,30'),
        ('17:00', '17,00'),
        ('17:30', '17,30'),
        ('18:00', '18,00'),
        ('18:30', '18,30'),
        ('19:00', '19,00'),
        ('19:30', '19,30'),
        ('20:00', '20,00'),
        ('20:30', '20,30'),
        ('21:00', '21,00'),
        ('21:30', '21,30'),
        ('22:00', '22,00'),
        ('22:30', '22,30'),
        ('23:00', '23,00'),
        ('23:30', '23,30'),
        ('24:00', '24,00'),
)


class Place(models.Model):
    """
    This class represents a place.
    @version: 1.0
    """
    id = UuidField(primary_key=True)
    label = models.CharField(max_length=80)
    active = models.BooleanField(default=True)
    address = generic.GenericRelation(Address)
    phones = generic.GenericRelation(Phone)
    place_type = models.ForeignKey(PlaceType)
    organization = models.ForeignKey(Organization, null=True, blank=True)
    comments = models.TextField(blank=True, null=True)

    hour_start = models.CharField(u'Primeiro horário', max_length=10,
                                  default='07,00', choices=HOURS)
    hour_end = models.CharField(u'Último horário', max_length=10,
                                default='19,00', choices=HOURS)

    objects = PlaceManager()

    def __unicode__(self):
        return "%s" % self.label

    def __str__(self):
        return "%s" % self.label

    def __empty__(self):
        return ''
    area = property(__empty__)
    addressPrefix = property(__empty__)
    addressLine1 = property(__empty__)
    addressLine2 = property(__empty__)
    addressNumber = property(__empty__)
    neighborhood = property(__empty__)
    zipCode = property(__empty__)
    addressType = property(__empty__)

    def get_first_phone(self):
        if (len(self.phones.all()) != 0):
            return self.phones.all()[0]
        else:
            return ''

    def occurrences(self):
        o = []
        for room in self.room_set.filter(active=True):
            for i in room.scheduleoccurrence_set.filter(
                start_time__gte=datetime.now()).exclude(
                    occurrenceconfirmation__presence=4).exclude(
                    occurrenceconfirmation__presence=5):
                o.append(i)
        return o

    class Meta:
        ordering = ['label']
        permissions = (
            ("place_add", "Can add places"),
            ("place_change", "Can change places"),
            ("place_list", "Can list places"),
            ("place_write", "Can write places"),
        )

    def revision(self):
        return reversion.get_for_object(self).order_by(
            '-revision__date_created').latest(
            'revision__date_created').revision

    # Tiago de Souza Moraes, 26/11/2013
    # retorna a quantidade de horas que a sala estará aberta para atendimento
    # return array = [hour_start], [min_start], [hours_works]
    def hours_work(self):
        r = [None]*3

        # hour
        r[0] = (int(self.hour_start.split(',')[0]))
        # min
        r[1] = (int(self.hour_start.split(',')[1]))

        # quantas horarios disponivel na agenda
        m = 0
        # meia hora existe?
        if int(self.hour_start.split(',')[1]) > int(self.hour_end.split(
                                                    ',')[1]):
            m = float(-.5)

        if int(self.hour_start.split(',')[1]) < int(self.hour_end.split(
                                                    ',')[1]):
            m = float(.5)

        x = (float(self.hour_end.split(',')[0]) - float(self.hour_start.split(
                                                        ',')[0])) + m

        r[2] = x
        return r

reversion.register(Place, follow=['address', 'phones'])


class RoomType(models.Model):
    """
    This class contains information on room types, thus instances of this class
    can be used to handle information related to room types.
    @version: 1.0
    """
    description = models.CharField(max_length=45, unique=True)

    def __unicode__(self):
        return "%s" % self.description

    def __str__(self):
        return "%s" % self.description

    class Meta:
        ordering = ['description']


class RoomManager(models.Manager):
    def active(self):
        return super(RoomManager, self).get_query_set().filter(active=True)

    def deactive(self):
        return super(RoomManager, self).get_query_set().filter(active=False)


class Room(models.Model):
    """
    This class represents a room, it also holds information on the furniture
    that belongs to the underlying room and its dimension.
    @version: 1.0
    """
    id = UuidField(primary_key=True)
    description = models.CharField(max_length=80, blank=True)
    dimension = models.CharField(max_length=10, blank=True)
    place = models.ForeignKey(Place)
    room_type = models.ForeignKey(RoomType, related_name='room_type')
    furniture = models.TextField()
    active = models.BooleanField(default=True)
    comments = models.TextField(blank=True)

    objects = RoomManager()

    class Meta:
        ordering = ['description']

    def __unicode__(self):
        return "%s" % self.description

    def __str__(self):
        return "%s" % self.description

    def __empty__(self):
        return ''
    area = property(__empty__)
    addressPrefix = property(__empty__)
    addressLine1 = property(__empty__)
    addressPrefix = property(__empty__)
    addressLine1 = property(__empty__)
    addressLine2 = property(__empty__)
    addressNumber = property(__empty__)
    neighborhood = property(__empty__)
    zipCode = property(__empty__)
    addressType = property(__empty__)

    def revision(self):
        return reversion.get_for_object(self).order_by(
            '-revision__date_created').latest(
            'revision__date_created').revision

    def is_busy(self, start_time, end_time):
        ''' check if room is busy in schedule for selected range '''
        ''' filter 1: start time not in occurrence range '''
        ''' filter 2: end time not in occurrence range '''
        ''' filter 2: end time not in occurrence range '''
        ''' filter 3: occurrence range are not between asked values '''

        from gestorpsi.schedule.models import ScheduleOccurrence
        queryset = ScheduleOccurrence.objects.filter(
            room=self).exclude(occurrenceconfirmation__presence=4).exclude(
            occurrenceconfirmation__presence=5)

        return True if \
            queryset.filter(start_time__lte=start_time,
                            end_time__gt=start_time) or \
            queryset.filter(start_time__lt=end_time,
                            end_time__gte=end_time) or \
            queryset.filter(start_time__gte=start_time,
                            end_time__lte=end_time) \
            else False

    def occurrences(self):
        o = []
        for i in self.scheduleoccurrence_set.filter(
            start_time__gte=datetime.now()).exclude(
            occurrenceconfirmation__presence=4).exclude(
                occurrenceconfirmation__presence=5):
                o.append(i)
        return o

reversion.register(Room)
