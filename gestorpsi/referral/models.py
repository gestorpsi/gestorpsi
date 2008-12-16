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
from gestorpsi.client.models import Client
from gestorpsi.service.models import Service
from gestorpsi.careprofessional.models import CareProfessional
from gestorpsi.util.uuid_field import UuidField

class Referral(models.Model):
    id = UuidField(primary_key=True)
    client = models.ForeignKey(Client)
    professional = models.ForeignKey(CareProfessional, null=True)
    service = models.ForeignKey(Service, null=True)
    creation_datetime = models.DateTimeField(auto_now_add=True)
    user = models.CharField(max_length=10, blank=True)

    def __unicode__(self):
        return u"\nClient: %s\nProfessional: %s\nService: %s" % (self.client, self.professional, self.service)
