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
from gestorpsi.util.uuid_field import UuidField
from gestorpsi.referral.models import Referral
from gestorpsi.place.models import Room

class Schedule(models.Model):
    id = UuidField(primary_key=True)
    referral = models.ForeignKey(Referral)
    room = models.ForeignKey(Room, null=True)
    appointment_begin = models.DateTimeField()
    appointment_end = models.DateTimeField()

    def __unicode__(self):
        return u"\nClient: %s\nProfessional: %s\nRoom: %s\nService: %s\nBegin: %s\nEnd: %s\n" % (self.referral.client, self.referral.professional, self.room, self.referral.service, self.appointment_begin, self.appointment_end)