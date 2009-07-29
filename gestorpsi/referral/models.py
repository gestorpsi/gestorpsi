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
from datetime import datetime
from django.db import models
from django.utils.translation import ugettext as _
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

REFERRAL_DISCHARGE_TYPE = (
    ('1', _('Abandonment of service ')),
    ('2', _('Withdrawal of service - Tried the other type of treatment')),
    ('3', _('Withdrawal of service - The shutdown was reported by the ')),
    ('4', _('Withdrawal of service - The incompatibility of schedule ')),
    ('5', _('Unable to contact the customer')),
    ('6', _('Abandonment / withdrawal from the (a) professional')),
    ('7', _('High * (end of the process without the professional)')),
    ('8', _('Referral to external continuity of treatment ')),
    ('9', _('Death of the Client ')),
    ('10', _('Death of the professional ')),
    ('11', _('Default/Neglect')),
    ('12', _('Change of city/address ')),
    ('13', _('Do not attended the first consultation')),
    ('14', _('Not informed')),
    ('15', _('End stage - the case was closed')),
    ('16', _('Treatment / Service terminated by court order')),
    ('17', _('Other')),
)

REFERRAL_DISCHARGE_STATUS = (
    ('1', _('Authorization')),
    ('2', _('List of expected')),
    ('3', _('Scheduled')),
    ('4', _('In attendance (active)')),
    ('5', _('Forwarded to external service and remains in attendance at the clinic (active)')),
    ('6', _('Inactive')),
    ('7', _('Off')),
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

class ReferralManager(models.Manager):
    def charged(self):
        return super(ReferralManager, self).get_query_set().filter(referraldischarge__isnull=True)

    def discharged(self):
        return super(ReferralManager, self).get_query_set().filter(referraldischarge__isnull=False)
    


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

    objects = ReferralManager()

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

    def is_discharged(self):
        if len(self.referraldischarge_set.all()) > 0:
            return True
        else:
            return False

    def past_occurrences(self):
        '''
        Return all past occurrences
        '''
        return self.occurrence_set.filter(start_time__lt=datetime.now())

class ReferralDischarge(models.Model):
    id = UuidField(primary_key=True)
    referral = models.ForeignKey(Referral, null=False, blank=False)
    client = models.ForeignKey(Client, null=True, blank=True)
    group = models.ForeignKey(ReferralGroup, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    was_discussed_with_client =  models.BooleanField(_('Was Discussed With Client'), default=False)
    reason = models.CharField(_('Discharge Reason'), max_length=2, blank=True, null=True, choices=REFERRAL_DISCHARGE_TYPE)
    details = models.TextField(_('Discharge Details'), blank=True)
    status = models.CharField(_('Status'), max_length=2, blank=True, null=True, choices=REFERRAL_DISCHARGE_STATUS)
    description = models.TextField(_('Comments'), blank=True)
    
    def __unicode__(self):
        return u'%s - %s' % (self.client, self.referral.service)

    class Meta:
        ordering = ['-date','client']

reversion.register(Event)
reversion.register(ReferralDischarge, follow=['referral'])
reversion.register(Referral, follow=['event_ptr'])
reversion.register(ReferralGroup, follow=['referral'])
