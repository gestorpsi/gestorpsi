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

from dateutil import rrule
from django.db import models
from swingtime.models import Event, EventType
from gestorpsi.client.models import Client
from gestorpsi.service.models import Service
from gestorpsi.careprofessional.models import CareProfessional
from gestorpsi.util.uuid_field import UuidField
from gestorpsi.schedule.models import ScheduleOccurrence

class Referral(Event):
    #id = UuidField(primary_key=True)
    client = models.ManyToManyField(Client)
    professional = models.ManyToManyField(CareProfessional, null=True)
    service = models.ForeignKey(Service, null=True)
    annotation = models.CharField(max_length=765, null=True, blank=True)

    def __init__(self, *args, **kwargs):
        super(Referral, self).__init__(*args, **kwargs)
        try: self.event_type = EventType.objects.all()[0]
        except: self.event_type = EventType.objects.create(abbr='')

    def add_occurrences(self, start_time, end_time, room, **rrule_params):
        rrule_params.setdefault('freq', rrule.DAILY)

        if 'count' not in rrule_params and 'until' not in rrule_params:
            ScheduleOccurrence.objects.create(event=self, start_time=start_time, end_time=end_time, room_id=room)
        else:
            delta = end_time - start_time
            for ev in rrule.rrule(dtstart=start_time, **rrule_params):
                ScheduleOccurrence.objects.create(event=self, start_time=ev, end_time=ev + delta, room_id=room)
                
    class Meta:
        ordering = ('title', )

    def __unicode__(self):
        return u"\nClient: %s\nProfessional: %s\nService: %s" % (self.client, self.professional, self.service)
