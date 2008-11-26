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

from django.db import models
from gestorpsi.organization.models import Organization
from gestorpsi.careprofessional.models import CareProfessional


class ReferralChoice(models.Model):
    description = models.CharField(max_length=50)
    def __unicode__(self):
        return u"%s" % self.description

class Referral(models.Model):
    referral_choice = models.ForeignKey(ReferralChoice)
    referral_organization = models.ForeignKey(Organization, null=True)
    referral_professional = models.ForeignKey(CareProfessional, null=True)
    def __unicode__(self):
        return u"%s" % self.description

class IndicationChoice(models.Model):
    description = models.CharField(max_length=50)
    def __unicode__(self):
        return u"%s" % self.description

class Indication(models.Model):
    indication_choice = models.ForeignKey(IndicationChoice)
    referral_organization = models.ForeignKey(Organization, null=True)
    referral_professional = models.ForeignKey(CareProfessional, null=True)
    def __unicode__(self):
        return u"%s" % self.description