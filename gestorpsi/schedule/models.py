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
from swingtime.models import Event, EventType, Occurrence
from gestorpsi.service.models import Service
from gestorpsi.careprofessional.models import CareProfessional
from gestorpsi.client.models import Client
from gestorpsi.place.models import Place, Room
from gestorpsi.device.models import DeviceDetails


class ScheduleOccurrence(Occurrence):
    room = models.ForeignKey(Room, null=True, blank=True)
    device = models.ManyToManyField(DeviceDetails, null=True, blank=True)
    annotation = models.CharField(max_length=765, null=True, blank=True)


