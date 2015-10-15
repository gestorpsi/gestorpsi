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
from django.test import TestCase

from .models import TimeUnit, Demand
from gestorpsi.client.models import Client
from gestorpsi.schedule.models import ScheduleOccurrence
from gestorpsi.referral.models import Referral
from datetime import datetime



class DemandTest(TestCase):
	def setUp(self):
		timeunit = TimeUnit(unit="u", time="time")
		clientD = Client()
		referralD = Referral()
		scheduleD = ScheduleOccurrence()

		self.demandD = Demand(date_created=datetime(2015, 10, 15, 12, 12, 12),
							 date_modified=datetime(2015, 10, 15, 13, 13, 13),
							 edit_status="edit", initial_complaint=True, demand="demand",
							 description="desc", how_long_it_happens=timeunit, frequency=timeunit,
							 severity="severity", duration=timeunit, demand_status = "status",
							 demand_resolution=datetime(2015, 10, 15, 13, 13, 13), bibliography="bibliography",
							 related_sites="related_sites", comments="comments",
							 client=clientD, referral=referralD, occurrence=scheduleD)

		self.demand = "demand"

	def testUnicode(self):
		self.assertEquals(self.demand, unicode(self.demandD))
