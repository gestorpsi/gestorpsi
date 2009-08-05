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
from django.utils.translation import ugettext as _
from swingtime.models import Occurrence
from gestorpsi.place.models import Room
from gestorpsi.device.models import DeviceDetails

OCCURRENCE_CONFIRMATION_PRESENCE = (
    ('1', _('Arrived on time')),
    ('2', _('Arrived Late')),
    ('3', _('Not arrive')),
)

class ScheduleOccurrence(Occurrence):
    room = models.ForeignKey(Room, null=True, blank=True)
    device = models.ManyToManyField(DeviceDetails, null=True, blank=True)
    annotation = models.CharField(max_length=765, null=True, blank=True)

    #def is_past(self):
        #if self.start_time < datetime.now():
            #return True
        #else:
            #return False

    def is_past(self):
        return self.start_time < datetime.now() or None

    def revision(self):
        return reversion.models.Version.objects.get_for_object(self).order_by('-revision__date_created').latest('revision__date_created').revision

class OccurrenceConfirmation(models.Model):
    occurrence = models.OneToOneField(ScheduleOccurrence)
    date_started = models.DateTimeField(_('Occurrence Date Started'), blank=True)
    presence = models.CharField(_('Presence Confirmation'), max_length=2, blank=True, choices=OCCURRENCE_CONFIRMATION_PRESENCE)
    unmarked = models.BooleanField(_('Occurrence Unmarked'), default = False)
    remarked = models.BooleanField(_('Occurrence Rescheduled'), default = False)
    reason = models.TextField(_('Unmark or Reschedule Reason (if exists)'), blank = True)
    comments = models.TextField(_('Aditional Comments'), blank = True)

    def __unicode__(self):
        return self.occurrence.event.referral.service.name

reversion.register(Occurrence)
reversion.register(ScheduleOccurrence, follow=['occurrence_ptr'])

