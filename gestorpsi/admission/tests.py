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
from .models import ReferralChoice, AdmissionManager, AdmissionInRangeManager, AdmissionReferral, Attach

class ReferralChoiceTest(TestCase):
	def setUp(self):
		self.referralchoice = ReferralChoice(description="Hu3Hu3")
		self.description = "Hu3Hu3"

	def testUnicode(self):
		self.assertEquals(self.description, unicode(self.referralchoice))

	def testUnicodeFalse(self):
		self.assertNotEquals("False", unicode(self.referralchoice))



class AdmissionManager(TestCase):
	def setUp(self):
		pass

class AdmissionInRangeManager(TestCase):
	def setUp(self):
		pass

class AdmissionReferral(TestCase):
	def setUp(self):
		pass

class Attach(TestCase):
	def setUp(self):
		pass