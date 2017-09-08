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
from django.utils.translation import ugettext as _

from gestorpsi.organization.models import Organization
from gestorpsi.careprofessional.models import CareProfessional
from gestorpsi.client.models import Client
from gestorpsi.util.uuid_field import UuidField


ATTACH_TYPE = (
    ('01', _('Termo de Consentimento Livre e Esclarecido (TCLE)')),
)

class ReferralChoice(models.Model):
    description = models.CharField(max_length=250)
    nick = models.CharField(max_length=50, blank=True)
    weight = models.IntegerField(blank=True, null=True)
    color = models.CharField(_('Color'), max_length=6, null=True, help_text=_('Color in HEX Format. Ex: 662393'))

    def __unicode__(self):
        return u"%s" % self.description

    class Meta:
        ordering = ['weight']

class AdmissionManager(models.Manager):
    def inrange(self, organization, datetime_start=None, datetime_end=None):
        """
        filter admissions by logged organization, date start and date end
        if not provided 'date start' set it as the creation date of the organization
        if not provided 'date end' set it as now
        """

        if not datetime_start or not datetime_end:
            datetime_start = organization.created()
            datetime_end = datetime.now()

        inrange = []
        for a in super(AdmissionManager, self).get_query_set().filter(client__person__organization=organization):
            if a.created >= datetime_start and a.created <= datetime_end:
                inrange.append(a.id)

        return AdmissionReferral.objects.filter(pk__in=inrange)

    #def signed(self, organization, query_pk_in=None):
        #q = super(AdmissionManager, self).get_query_set().filter(client__person__active=True, signed_bythe_client=True, client__person__organization=organization)
        #if query_pk_in:
            #q = q.filter(pk__in=query_pk_in)
        #return q

    #def not_signed(self, organization, query_pk_in=None):
        #q = super(AdmissionManager, self).get_query_set().filter(client__person__active=True, signed_bythe_client=False, client__person__organization=organization)
        #if query_pk_in:
            #q = q.filter(pk__in=query_pk_in)
        #return q

class AdmissionInRangeManager(models.Manager):
    """
    this manager has been created as a help
    to provide data to use in 'report' app
    """
    
    def all(self, organization, datetime_start=None, datetime_end=None):
        return AdmissionReferral.objects.inrange(organization, datetime_start, datetime_end)

class AdmissionReferral(models.Model):
    id = UuidField(primary_key=True)
    referral_choice = models.ForeignKey(ReferralChoice)
    referral_organization = models.ForeignKey(Organization, null=True)
    referral_professional = models.ForeignKey(CareProfessional, null=True)
    signed_bythe_client = models.BooleanField(default=False)
    client = models.ForeignKey(Client)
    date = models.DateTimeField(auto_now_add=True)
    
    objects = AdmissionManager()
    objects_inrange = AdmissionInRangeManager()
    
    def __unicode__(self):
        return u'%s' % self.client
    
    def revision(self):
        return reversion.get_for_object(self).order_by('-revision__date_created').latest('revision__date_created').revision
    
    def revision_created(self):
        return reversion.get_for_object(self).order_by('revision__date_created').latest('revision__date_created').revision

    def created_revision(self):
        return self.revision_created().date_created

    def _created(self):
        return self.date
    created = property(_created)

reversion.register(AdmissionReferral, follow=['client'])

class Attach(models.Model):
    filename = models.CharField(null=True, max_length=255)
    description = models.TextField(null=True)
    date = models.DateTimeField(auto_now_add=True)
    file = models.CharField(max_length=200)
    type = models.CharField(max_length=2, blank=True, null=True, choices=ATTACH_TYPE) 
    client = models.ForeignKey(Client)

    def __unicode__(self):
        return u'%s' % (self.file)
