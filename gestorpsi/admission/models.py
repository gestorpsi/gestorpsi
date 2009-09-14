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
from django.db import models
from gestorpsi.organization.models import Organization
from gestorpsi.careprofessional.models import CareProfessional
from gestorpsi.client.models import Client
from gestorpsi.util.uuid_field import UuidField

class ReferralChoice(models.Model):
    description = models.CharField(max_length=250)
    nick = models.CharField(max_length=50, blank=True)
    weight = models.IntegerField(blank=True, null=True)

    def __unicode__(self):
        return u"%s" % self.description

    class Meta:
        ordering = ['weight']

class AdmissionReferral(models.Model):
    id = UuidField(primary_key=True)
    referral_choice = models.ForeignKey(ReferralChoice)
    referral_organization = models.ForeignKey(Organization, null=True)
    referral_professional = models.ForeignKey(CareProfessional, null=True)
    client = models.ForeignKey(Client)
    
    def __unicode__(self):
        return u"%s - %s" % (self.client, self.referral_choice)
    
    def revision(self):
        return reversion.models.Version.objects.get_for_object(self).order_by('-revision__date_created').latest('revision__date_created').revision

reversion.register(AdmissionReferral, follow=['client'])
