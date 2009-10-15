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
        return super(ScheduleOccurrenceManager, self).get_query_set().filter(start_time__lt = datetime.now(), occurrenceconfirmation__isnull = False)
    
    def not_confirmed(self):
        return super(ScheduleOccurrenceManager, self).get_query_set().filter(start_time__lt = datetime.now(), occurrenceconfirmation__isnull = True)
    
    def unmarked(self):
        return super(ScheduleOccurrenceManager, self).get_query_set().filter(Q(occurrenceconfirmation__presence=4) | Q(occurrenceconfirmation__presence=5))
    
    def not_unmarked(self):
        return super(ScheduleOccurrenceManager, self).get_query_set().exclude(occurrenceconfirmation__presence=4).exclude(occurrenceconfirmation__presence=5)

class ScheduleOccurrence(Occurrence):
    room = models.ForeignKey(Room, null=True, blank=True)
    device = models.ManyToManyField(DeviceDetails, null=True, blank=True)
    annotation = models.CharField(max_length=765, null=True, blank=True)

    objects = ScheduleOccurrenceManager()

    def is_past(self):
        return True if self.start_time < datetime.now() else False
    
    def was_confirmed(self):
        return True if len(OccurrenceConfirmation.objects.filter(occurrence=self)) else False

    def revision(self):
        return reversion.models.Version.objects.get_for_object(self).order_by('-revision__date_created').latest('revision__date_created').revision

class OccurrenceConfirmation(models.Model):
    occurrence = models.OneToOneField(ScheduleOccurrence)
    date_started = models.DateTimeField(_('Occurrence Date Started'), blank=True, null=True)
    date_finished = models.DateTimeField(_('Occurrence Date Finished'), blank=True, null=True)
    presence = models.IntegerField(_('Presence Confirmation'), max_length=2, blank=True, null=True, choices=OCCURRENCE_CONFIRMATION_PRESENCE)
    reason = models.TextField(_('Unmark or Reschedule Reason (if exists)'), blank = True)
    device = models.ManyToManyField(DeviceDetails, null=True, blank=True)

    def __unicode__(self):
        return u'%s' % self.get_presence_display()

reversion.register(Occurrence)
reversion.register(ScheduleOccurrence, follow=['occurrence_ptr'])

reversion.register(OccurrenceConfirmation, follow=['occurrence'])

