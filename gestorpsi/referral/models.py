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
from django.core.files import File
from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext as _
from django.core.files.storage import FileSystemStorage
from swingtime.models import Event, EventType
from gestorpsi.client.models import Client
from gestorpsi.service.models import Service
from gestorpsi.careprofessional.models import CareProfessional
from gestorpsi.schedule.models import ScheduleOccurrence
from gestorpsi.organization.models import Organization
from gestorpsi.util.uuid_field import UuidField
from gestorpsi.place.models import Room

fs = FileSystemStorage(location='/tmp')

class ReferralPriority(models.Model):
    title = models.CharField(max_length=20)
    
    def __unicode__(self):
        return u'%s' % self.title

class ReferralImpact(models.Model):
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=765, null=True, blank=True)
    
    def __unicode__(self):
        return u'%s (%s)' % (self.title, self.description)

QUEUE_PRIORITY= (
    ('01', _('High')),
    ('02', _('Medium')),
    ('03', _('Low')),
)

REFERRAL_ATTACH_TYPE = (
    ('01', _('Drawing')),
    ('02', _('Diagnosis')),
    ('03', _('Medical Examination')),
    ('04', _('Reference')),
    ('05', _('Results sheet')),
    ('06', _('Test sheet')),
    ('07', _('Photo')),
    ('08', _('Laudo')),
    ('09', _('Parecer')),
    ('10', _('Termo de Consentimento Livre e Esclarecido (TCLE)')),
    ('11', _('Others')),
)


REFERRAL_STATUS = (
    ('01', _('Active')),
    ('02', _('Inactive')),
    ('03', _('Unknown')),
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
    ('17', _('Internal referral')),
    ('18', _('Other')),
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
    active = models.BooleanField(default=True)
    
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

class Queue(models.Model):
    comments = models.TextField(_('comments'), blank=True)
    date_in = models.DateTimeField(_('Data In'), auto_now_add=True)
    date_out = models.DateTimeField(_('Data Out'), null=True, blank=True)
    priority = models.CharField(_('Priority'), max_length=2, blank=True, choices=QUEUE_PRIORITY, default='03') 
    client = models.ForeignKey(Client)
    referral = models.ForeignKey('Referral')

    def __unicode__(self):
        return u'%s' % (self.priority)

class ReferralAttach(models.Model):
    id = UuidField(primary_key=True)
    filename = models.CharField(null=True, max_length=255)
    description = models.TextField(null=True)
    date = models.DateTimeField(auto_now_add=True)
    file = models.CharField(max_length=200)
    type = models.CharField(max_length=2, blank=True, null=True, choices=REFERRAL_ATTACH_TYPE) 
    referral = models.ForeignKey('Referral')

    def __unicode__(self):
        return u'%s' % (self.file)

class Referral(Event):
    #id = UuidField(primary_key=True)
    client = models.ManyToManyField(Client, null=True, blank=True)
    professional = models.ManyToManyField(CareProfessional, null=True)
    service = models.ForeignKey(Service, null=True)
    referral = models.ForeignKey('Referral', null=True, blank=True, related_name='referral_children')
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

    def add_occurrences(self, start_time, end_time, room, device, annotation, is_online, **rrule_params):
        rrule_params.setdefault('freq', rrule.DAILY)

        error_list = []
        if 'count' not in rrule_params and 'until' not in rrule_params:
            is_busy = self.check_busy(start_time, end_time, room)
            if not is_busy:
                o = ScheduleOccurrence.objects.create(event=self, start_time=start_time, end_time=end_time, room_id=room, annotation=annotation)
                o.device = device
                o.is_online = is_online
                o.save()
            else:
                error_list.append(is_busy)
        else:
            delta = end_time - start_time
            for ev in rrule.rrule(dtstart=start_time, **rrule_params):
                is_busy = self.check_busy(ev, (ev + delta), room)
                if not is_busy:
                    o = ScheduleOccurrence.objects.create(event=self, start_time=ev, end_time=ev + delta, room_id=room, annotation=annotation)
                    o.device = device
                    o.is_online = is_online
                    o.save()
                else:
                    error_list.append(is_busy)
        
        return error_list

    def check_busy(self, start_time, end_time, room_id):
        room = Room.objects.get(pk=room_id)

        error_message = []
        if room.is_busy(start_time, end_time):
            error_message.append(_('%s is busy in this range') % room)

        for p in self.professional.all():
            if p.is_busy(start_time, end_time):
                error_message.append(_('Professional %s is busy in this range') % p)

        for c in self.client.all():
            if c.is_busy(start_time, end_time):
                error_message.append(_('Client %s is busy in this range') % c)
        
        if not error_message:
            return None
        else:
            return {
                'start_time': start_time, 
                'end_time': end_time, 
                'room': room, 
                'error_message': error_message
                }

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

    def past_occurrences(self):
        '''
        Return all past occurrences
        '''
        return self.occurrence_set.filter(start_time__lt=datetime.now()
            ).exclude(scheduleoccurrence__occurrenceconfirmation__presence = 4 # unmarked
            ).exclude(scheduleoccurrence__occurrenceconfirmation__presence = 5 # re-marked
            ).exclude( Q(scheduleoccurrence__is_online=True) & Q(end_time__gt=datetime.now())
            ).reverse()

    def online_and_active_occurrences(self):
        '''
        Return all occurrences that are active and that are online
        '''
        return self.occurrence_set.filter(start_time__lt=datetime.now()).filter(Q(scheduleoccurrence__is_online=True) & Q(end_time__gt=datetime.now())).reverse()

    def last_occurrence(self):
        past = self.past_occurrences()
        return past and past[0] or None

    def professional_list(self):
        a = []
        for p in self.professional.all():
            if(p.professionalIdentification.profession):
                a.append(u'%s (%s)' % (p, p.professionalIdentification.profession))
            else:
                a.append(u'%s' % (p))
        return a

    def upcoming_occurrences(self):
        return self.occurrence_set.filter(start_time__gte=datetime.now()
            ).exclude(scheduleoccurrence__occurrenceconfirmation__presence = 4 # unmarked
            ).exclude(scheduleoccurrence__occurrenceconfirmation__presence = 5) # re-marked

    def on_queue(self):
        return True if self.queue_set.filter(date_out__isnull=True) else False

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

class IndicationChoice(models.Model):
    description = models.CharField(max_length=250)
    nick = models.CharField(max_length=50, blank=True)
    weight = models.IntegerField(blank=True, null=True)

    def __unicode__(self):
        return u"%s" % self.description

    class Meta:
        ordering = ['weight']

class Indication(models.Model):
    id = UuidField(primary_key=True)
    indication_choice = models.ForeignKey(IndicationChoice, null=False)
    referral = models.ForeignKey(Referral)
    referral_organization = models.ForeignKey(Organization, null=True)
    referral_professional = models.ForeignKey(CareProfessional, null=True)

    def __unicode__(self):
        return u"%s" % self.indication_choice

    def revision(self):
        return reversion.models.Version.objects.get_for_object(self).order_by('-revision__date_created').latest('revision__date_created').revision

reversion.register(Indication, follow=['client'])

class ReferralChoice(models.Model):
    description = models.CharField(max_length=250)
    nick = models.CharField(max_length=50)
    def __unicode__(self):
        return u"%s" % self.description

class ReferralReferral(models.Model):
    id = UuidField(primary_key=True)
    referral_choice = models.ForeignKey(ReferralChoice)
    referral_organization = models.ForeignKey(Organization, null=True)
    referral_professional = models.ForeignKey(CareProfessional, null=True)
    client = models.ForeignKey(Client)

    def __unicode__(self):
        return u"%s" % self.referral_choice

    def revision(self):
        return reversion.models.Version.objects.get_for_object(self).order_by('-revision__date_created').latest('revision__date_created').revision

reversion.register(ReferralReferral, follow=['client'])

class ReferralExternal(models.Model):
    comments = models.TextField(_('comments'), blank=True)
    date = models.DateTimeField(_('Data'), auto_now_add=True)
    referral = models.ForeignKey('Referral')
    organization = models.ForeignKey(Organization, null=True)
    professional = models.ForeignKey(CareProfessional, null=True)
