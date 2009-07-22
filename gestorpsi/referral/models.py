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
from dateutil import rrule
from django.db import models
from swingtime.models import Event, EventType
from gestorpsi.client.models import Client
from gestorpsi.service.models import Service
from gestorpsi.careprofessional.models import CareProfessional
from gestorpsi.schedule.models import ScheduleOccurrence
from gestorpsi.organization.models import Organization
from gestorpsi.util.uuid_field import UuidField

class ReferralPriority(models.Model):
    title = models.CharField(max_length=20)
    
    def __unicode__(self):
        return u'%s' % self.title

class ReferralImpact(models.Model):
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=765, null=True, blank=True)
    
    def __unicode__(self):
        return u'%s (%s)' % (self.title, self.description)

REFERRAL_STATUS = (
    ('01', 'Active'),
    ('02', 'Inactive'),
    ('03', 'Unknown'),
)

class ReferralGroup(models.Model):
    id = UuidField(primary_key=True)
    referral = models.ForeignKey('Referral', null=True, blank=True)
    description = models.CharField(max_length=100)
    comments = models.TextField(blank=True)
    #active = models.BooleanField(default=True)
    
    def __unicode__(self):
        return u'%s' % (self.description)

    class Meta:
        ordering = ['referral__service__name', 'description']

    def revision(self):
        return reversion.models.Version.objects.get_for_object(self).order_by('-revision__date_created').latest('revision__date_created').revision

class Referral(Event):
    #id = UuidField(primary_key=True)
    client = models.ManyToManyField(Client, null=True, blank=True)
    professional = models.ManyToManyField(CareProfessional, null=True)
    service = models.ForeignKey(Service, null=True)
    referral = models.ForeignKey('Referral', null=True, blank=True, related_name='referral_parent')
    date = models.DateTimeField(auto_now_add=True)
    referral_reason = models.CharField(max_length=765, null=True, blank=True)
    annotation = models.CharField(max_length=765, null=True, blank=True)
    available_time = models.CharField(max_length=765, null=True, blank=True)
    priority = models.ForeignKey(ReferralPriority, null=True)
    impact = models.ForeignKey(ReferralImpact, null=True)
    organization = models.ForeignKey(Organization, null= True, blank= True)
    status = models.CharField(max_length=2, blank=True, null=True, choices=REFERRAL_STATUS)

    def __init__(self, *args, **kwargs):
        super(Referral, self).__init__(*args, **kwargs)
        try: self.event_type = EventType.objects.all()[0]
        except: self.event_type = EventType.objects.create(abbr='')

    def add_occurrences(self, start_time, end_time, room, device, **rrule_params):
        rrule_params.setdefault('freq', rrule.DAILY)
        if 'count' not in rrule_params and 'until' not in rrule_params:
            o = ScheduleOccurrence.objects.create(event=self, start_time=start_time, end_time=end_time, room_id=room)
            o.device = device
            o.save()
        else:
            delta = end_time - start_time
            for ev in rrule.rrule(dtstart=start_time, **rrule_params):
                o = ScheduleOccurrence.objects.create(event=self, start_time=ev, end_time=ev + delta, room_id=room)
                o.device = device
                o.save()

    class Meta:
        ordering = ('title', )

    def __unicode__(self):
        return u"%s" % (self.service)

    def revision(self):
        return reversion.models.Version.objects.get_for_object(self).order_by('-revision__date_created').latest('revision__date_created').revision

    def group_name(self):
        try:
            r = self.referralgroup_set.all()[0]
            return r.description
        except:
            return None

reversion.register(Event)
reversion.register(Referral, follow=['event_ptr'])
reversion.register(ReferralGroup, follow=['referral'])
