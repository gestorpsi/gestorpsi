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
from gestorpsi.address.models import Country, State, City
from django.test import TestCase

class CountryTest(TestCase):
	def setUp(self):
		self.country = Country(name="Brasil")
		self.name = "Brasil"

	def testUnicode(self):
		self.assertEquals(self.name, unicode(self.country))



