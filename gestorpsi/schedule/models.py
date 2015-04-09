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

from datetime import datetime
import reversion
from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext as _
from swingtime.models import Occurrence
from gestorpsi.place.models import Room
from gestorpsi.client.models import Client
from gestorpsi.device.models import DeviceDetails
from gestorpsi.util.uuid_field import UuidField

OCCURRENCE_CONFIRMATION_PRESENCE = (
    (1, _('Client arrived on time')),
    (2, _('Client arrived Late')),
    (3, _('Client not arrived')),
    (4, _('Occurrence unmarked')),
    (5, _('Occurrence rescheduled')),
)


class ScheduleOccurrenceManager(models.Manager):
    def confirmed(self):
        return super(ScheduleOccurrenceManager, self).get_query_set().filter(
            start_time__lt=datetime.now(),
            occurrenceconfirmation__isnull=False)

    def not_confirmed(self):
        return super(ScheduleOccurrenceManager, self).get_query_set().filter(
            start_time__lt=datetime.now(),
            occurrenceconfirmation__isnull=True)

    def unmarked(self):
        return super(ScheduleOccurrenceManager, self).get_query_set().filter(
            Q(occurrenceconfirmation__presence=4) |
            Q(occurrenceconfirmation__presence=5))

    def not_unmarked(self):
        return super(ScheduleOccurrenceManager, self).get_query_set().exclude(
            occurrenceconfirmation__presence=4).exclude(
            occurrenceconfirmation__presence=5)


class ScheduleOccurrenceRangeManager(models.Manager):
    """
    this manager has been created as a help
    to provide data to use in 'report' app
    """

    def all(self, organization, datetime_start=None, datetime_end=None):
        return ScheduleOccurrence.objects.filter(
            room__place__organization=organization,
            date__gte=datetime_start, date__lt=datetime_end)

    def in_place(self, place, datetime_start=None, datetime_end=None):
        return ScheduleOccurrence.objects.filter(
            room__place=place, date__gte=datetime_start, date__lt=datetime_end)

    def in_room(self, room, datetime_start=None, datetime_end=None):
        return ScheduleOccurrence.objects.filter(
            room=room, date__gte=datetime_start, date__lt=datetime_end)


class ScheduleOccurrence(Occurrence):
    """
    This class represents a "Scheduled Event". It can optionally relate a room,
    devices (none, one or many), it can has an annotation, and it has
    information about the type of the event - online or "in place". Online
    events are those scheduled and taked in an online manner - in general, it
    represents that one or more careprofessionals are taking the event online,
    using a computer in a room to take the online event.
    """
    room = models.ForeignKey(Room, null=True, blank=True)
    device = models.ManyToManyField(DeviceDetails, null=True, blank=True)
    reserve = models.BooleanField(default=False)
    annotation = models.CharField(max_length=765, null=True, blank=True)
    is_online = models.BooleanField(default=False)

    objects = ScheduleOccurrenceManager()
    objects_inrange = ScheduleOccurrenceRangeManager()

    def is_past(self):
        return True if self.start_time < datetime.now() else False

    def was_confirmed(self):
        return True if len(OccurrenceConfirmation.objects.filter(
            occurrence=self)) else False

    def online_users(self):

        if self.messagetopic_set.count() == 0:
            return 0

        messagetopic = self.messagetopic_set.all()[0]

        return messagetopic.online_users.count()

    def revision(self):
        return reversion.get_for_object(self).order_by(
            '-revision__date_created').latest(
                'revision__date_created').revision

    def __unicode__(self):
        return u"%s %s" % (datetime.strftime(
            self.start_time, '%d/%m/%Y %H:%M'), self.reserve)

    def have_company(self):
        have_company = False
        for i in self.event.referral.client.all():
            if i.person.is_company():
                have_company = True
        return have_company

    class Meta:
        ordering = ('start_time',)
        permissions = (
            ("schedule_list", "Can list occurrence confirmation"),
        )

    def employees_active(self):
        return self.occurrenceemployees.client.filter(active=True)

    def have_session(self):
        if hasattr(self, 'session'):
            return True
        return False

    def have_demand(self):
        if hasattr(self, 'demand'):
            return True
        return False

    def have_diagnosis(self):
        if hasattr(self, 'diagnosis'):
            return True
        return False

    def is_group(self):
        if self.event.referral.group:
            return True
        return False


class OccurrenceConfirmation(models.Model):
    occurrence = models.OneToOneField(ScheduleOccurrence)
    date_started = models.DateTimeField(_(
        'Occurrence Date Started'), blank=True, null=True)
    date_finished = models.DateTimeField(
        _('Occurrence Date Finished'), blank=True, null=True)
    presence = models.IntegerField(
        _('Presence Confirmation'), max_length=2, blank=True, null=True,
        choices=OCCURRENCE_CONFIRMATION_PRESENCE)
    reason = models.TextField(
        _('Unmark or Reschedule Reason (if exists)'), blank=True)
    device = models.ManyToManyField(DeviceDetails, null=True, blank=True)

    def __unicode__(self):
        return u'%s' % self.get_presence_display()


class OccurrenceFamily(models.Model):
    occurrence = models.OneToOneField(ScheduleOccurrence)
    client = models.ManyToManyField(Client, null=False, blank=False)

    def __unicode__(self):
        return u'%s: %s' % (self.occurrence, ", ".join(
            [c.person.name for c in self.client.all()]))


class OccurrenceEmployees(models.Model):
    occurrence = models.OneToOneField(ScheduleOccurrence)
    client = models.ManyToManyField(Client, null=False, blank=False)

    def __unicode__(self):
        return u'%s: %s' % (self.occurrence, ", ".join(
            [c.person.name for c in self.client.all()]))

reversion.register(Occurrence)
reversion.register(ScheduleOccurrence, follow=['occurrence_ptr'])
reversion.register(OccurrenceConfirmation, follow=['occurrence'])
reversion.register(OccurrenceFamily)
reversion.register(OccurrenceEmployees)
