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
from gestorpsi.settings import REFERRAL_DISCHARGE_REASON_CANCELED

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

REFERRAL_DISCHARGE_STATUS = (
    ('1', _('Authorization')),
    ('2', _('List of expected')),
    ('3', _('Scheduled')),
    ('4', _('In attendance (active)')),
    ('5', _('Forwarded to external service and remains in attendance at the clinic (active)')),
    ('6', _('Inactive')),
    ('7', _('Off')),
)

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
    only_professionals = models.BooleanField()
    only_psychologists = models.BooleanField()


    def __unicode__(self):
        return u'%s' % (self.file)

class ReferralInRangeManager(models.Manager):
    """
    this manager has been created as a help
    to provide data to use in 'report' app
    """
    
    def all(self, organization, datetime_start=None, datetime_end=None, service=None):
        r = Referral.objects.filter(service__organization=organization, date__gte=datetime_start, date__lt=datetime_end) \
            .exclude(referraldischarge__reason=REFERRAL_DISCHARGE_REASON_CANCELED)

        if service:
            r = r.filter(Q(service__pk=service) | Q(referral__service__pk=service))

        #if service:
            #r = r.filter(service__pk=service)

        return r

class Referral(Event):
    #id = UuidField(primary_key=True)
    seq = models.IntegerField(null=True, blank=True, max_length=5, default=0)
    client = models.ManyToManyField(Client, null=True, blank=True)
    professional = models.ManyToManyField(CareProfessional, null=True, blank=True)
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
    objects_inrange = ReferralInRangeManager()

    def __init__(self, *args, **kwargs):
        super(Referral, self).__init__(*args, **kwargs)
        try: self.event_type = EventType.objects.all()[0]
        except: self.event_type = EventType.objects.create(abbr='')
    
    def save(self, *args, **kwargs):
        is_new = True if not self.id else False
        super(Referral, self).save(*args, **kwargs)

        if is_new:
            self.seq = int(Referral.objects.filter(organization=self.organization).latest('seq').seq)+1
            self.save()
    
    def created_revision(self):
        return self.revision_created().date_created

    def _created(self):
        return self.date
    created = property(_created)

    def add_occurrences(self, start_time, end_time, room, device, annotation, is_online, disable_check_busy = False, reserve = False, **rrule_params):
        rrule_params.setdefault('freq', rrule.DAILY)
        error_list = []
        group = None
        if 'count' not in rrule_params and 'until' not in rrule_params:
            #adding_to_existing_group = False
            #try: # this try function is used to book a group. verify if the occurrence inserted is part from the same group
                #occurrence = ScheduleOccurrence.objects.filter(start_time=ev, end_time=ev + delta, room=Room.objects.get(pk=room))[0]
                #if occurrence.scheduleoccurrence.event.referral.group and occurrence.scheduleoccurrence.event.referral.group == self.group:
                    #adding_to_existing_group = True
            #except:
                #adding_to_existing_group = False

            is_busy = self.check_busy(start_time, end_time, room)
            #if not is_busy or adding_to_existing_group:
            if not is_busy or disable_check_busy:
                o = ScheduleOccurrence.objects.create(event=self, start_time=start_time, end_time=end_time, room_id=room, annotation=annotation)
                o.device = device
                o.is_online = is_online
                o.reserve = reserve
                o.save()
            else:
                error_list.append(is_busy)
        else:
            delta = end_time - start_time
            for ev in rrule.rrule(dtstart=start_time, **rrule_params):
                #adding_to_existing_group = False
                #try: # this try function is used to book a group. verify if the occurrence inserted is part from the same group
                    #occurrence = ScheduleOccurrence.objects.filter(start_time=ev, end_time=ev + delta, room=Room.objects.get(pk=room))[0]
                    #if occurrence.scheduleoccurrence.event.referral.group and occurrence.scheduleoccurrence.event.referral.group == self.group:
                        #adding_to_existing_group = True
                #except:
                    #adding_to_existing_group = False
                
                is_busy = self.check_busy(ev, (ev + delta), room)
                #if not is_busy or adding_to_existing_group:
                if not is_busy or disable_check_busy:
                    o = ScheduleOccurrence.objects.create(event=self, start_time=ev, end_time=ev + delta, room_id=room, annotation=annotation)
                    o.device = device
                    o.is_online = is_online
                    o.reserve = reserve
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
                'group': self.group, 
                'error_message': error_message,
                }

    class Meta:
        ordering = ('title', )
        permissions = (
            ("referral_add", "Can add referrals"),
            ("referral_change", "Can change referrals"),
            ("referral_list", "Can list referrals"),
            ("referral_write", "Can write referrals"),
        )

    def __unicode__(self):
        return u"%s #%s" % (self.service, self.seq)

    def _service_name_html(self):
        return u"<div class='service_name_html' style='background-color:#%s'>&nbsp;</div> %s #%s" % (self.service.color, self.service.name, self.seq)
    service_name_html = property(_service_name_html)

    def _service_name_html_inline(self):
        return u"%s #%s <div class='service_name_html_inline' style='background-color:#%s'>&nbsp;</div>" % (self.service.name, self.seq, self.service.color)
    service_name_html_inline = property(_service_name_html_inline)

    def revision(self):
        return reversion.get_for_object(self).order_by('-revision__date_created').latest('revision__date_created').revision

    def revision_created(self):
        return reversion.get_for_object(self).order_by('revision__date_created').latest('revision__date_created').revision

    def past_occurrences(self):
        '''
        Return all past occurrences without umarked and re-marked
        '''
        return self.occurrence_set.filter(start_time__lt=datetime.now()
            ).exclude(scheduleoccurrence__occurrenceconfirmation__presence = 4 # unmarked
            ).exclude(scheduleoccurrence__occurrenceconfirmation__presence = 5 # re-marked
            ).exclude( Q(scheduleoccurrence__is_online=True) & Q(end_time__gt=datetime.now())
            ).reverse()

    def past_occurrences_all(self):
        '''
        Return all occurrences
        '''
        return self.occurrence_set.filter(start_time__lt=datetime.now()).order_by('-start_time')

    def confirmed_occurrences(self):
        return self.occurrence_set.filter(scheduleoccurrence__occurrenceconfirmation__isnull=False)

    def unconfirmed_occurrences(self):
        return self.occurrence_set.filter(scheduleoccurrence__occurrenceconfirmation__isnull=True)

    def confirmed_arrive_ontime(self):
        return self.occurrence_set.filter(scheduleoccurrence__occurrenceconfirmation__isnull=False, scheduleoccurrence__occurrenceconfirmation__presence=1)

    def confirmed_arrive_late(self):
        return self.occurrence_set.filter(scheduleoccurrence__occurrenceconfirmation__isnull=False, scheduleoccurrence__occurrenceconfirmation__presence=2)

    def confirmed_not_arrived(self):
        return self.occurrence_set.filter(scheduleoccurrence__occurrenceconfirmation__isnull=False, scheduleoccurrence__occurrenceconfirmation__presence=3)

    def confirmed_unmarked(self):
        return self.occurrence_set.filter(scheduleoccurrence__occurrenceconfirmation__isnull=False, scheduleoccurrence__occurrenceconfirmation__presence=4)

    def confirmed_rescheduled(self):
        return self.occurrence_set.filter(scheduleoccurrence__occurrenceconfirmation__isnull=False, scheduleoccurrence__occurrenceconfirmation__presence=5)

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
            if(hasattr(p.professionalIdentification, "profession") and p.professionalIdentification.profession):
                a.append(u'%s (%s)' % (p, p.professionalIdentification.profession))
            else:
                a.append(u'%s' % (p))
        return a

    def upcoming_occurrences(self):
        return self.occurrence_set.filter(start_time__gte=datetime.now()
            ).exclude(scheduleoccurrence__occurrenceconfirmation__presence = 4 # unmarked
            ).exclude(scheduleoccurrence__occurrenceconfirmation__presence = 5) # re-marked

    def occurrences(self):
        return ScheduleOccurrence.objects.filter(event__referral=self)

    def on_queue(self):
        return True if self.queue_set.filter(date_out__isnull=True) else False

    def _group(self):
        from gestorpsi.service.models import GroupMembers
        if not hasattr(self.service,'is_group') or not self.service.is_group:
            return None
        else:
            if GroupMembers.objects.filter(referral=self):
                g = GroupMembers.objects.filter(referral=self)[0]
                return g.group if g else None
        return None
    
    group = property(_group)
    
    def occurrences_without_session(self):
        return self.occurrences().exclude(session__isnull=False).order_by('-start_time')

    def occurrences_without_demand(self):
        return self.occurrences().exclude(demand__isnull=False)

    def occurrences_without_diagnosis(self):
        return self.occurrences().exclude(diagnosis__isnull=False).order_by('-start_time')

class ReferralDischarge(models.Model):
    id = UuidField(primary_key=True)
    referral = models.ForeignKey(Referral, null=False, blank=False)
    client = models.ForeignKey(Client, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    was_discussed_with_client =  models.BooleanField(_('Was Discussed With Client'), default=False)
    #reason = models.CharField(_('Discharge Reason'), max_length=2, blank=True, null=True, choices=REFERRAL_DISCHARGE_TYPE)
    reason = models.ForeignKey('ReferralDischargeReason', verbose_name=('Discharge Reason'), blank=True, null=True)
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

class ReferralDischargeReason(models.Model):
    name = models.CharField(max_length=255)
    color = models.CharField(_('Color'), max_length=6, null=True, help_text=_('Color in HEX Format. Ex: 662393'))
    
    def __unicode__(self):
        return u'%s' % self.name
    
    class Meta:
        ordering = ['name',]

class IndicationChoice(models.Model):
    description = models.CharField(max_length=250)
    nick = models.CharField(max_length=50, blank=True)
    weight = models.IntegerField(blank=True, null=True)
    color = models.CharField(_('Color'), max_length=6, null=True, help_text=_('Color in HEX Format. Ex: 662393'))

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
        try:
            return u"%s" % self.indication_choice
        except:
            return ''

    def revision(self):
        return reversion.get_for_object(self).order_by('-revision__date_created').latest('revision__date_created').revision

reversion.register(Indication)

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
        return reversion.get_for_object(self).order_by('-revision__date_created').latest('revision__date_created').revision

reversion.register(ReferralReferral)

class ReferralExternal(models.Model):
    comments = models.TextField(_('comments'), blank=True)
    date = models.DateTimeField(_('Data'), auto_now_add=True)
    referral = models.ForeignKey('Referral')
    organization = models.ForeignKey(Organization, null=True)
    professional = models.ForeignKey(CareProfessional, null=True)
    
    def __unicode__(self):
        if self.professional:
            return u'%s - %s (%s)' % (self.date.strftime('%d/%m/%Y'), self.organization, self.professional)

        return u'%s - %s' % (self.date.strftime('%d/%m/%Y'), self.organization)
