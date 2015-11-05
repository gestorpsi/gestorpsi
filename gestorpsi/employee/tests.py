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

import reversion
from .models import EmployeeManager, Employee
from gestorpsi.person.models import Person
from gestorpsi.util.uuid_field import UuidField


class EmployeeManagerTest(TestCase):
	def setUp(self):
		# Active
		#In [6]: EmployeeManager.Active
		#Out[6]: <unbound method EmployeeManager.Active>

		# Deactive
		pass

class EmployeeTest(TestCase):
	def setUp(self):
		self.person = Person(name="personTest")
		uuidField = UuidField(verbose_name="verbose_name_Test", name="nameTest")
		self.employee = Employee(person=self.person, hiredate="HiredateTest", job="JobTest", active=True)
		
		self.hiredate = "hiredateTest"
		self.job = "jobTest"
		self.active = False

	def testUnicode(self):
		self.assertEqual(self.person.name, unicode(self.employee))
		self.assertEqual("hiredateTest", self.hiredate)
		self.assertEqual("jobTest", self.job)
		self.assertEqual(False, self.active)

	# Rollback and recovery facility to your admin site
	#def testRevision(self):
		#self.assertEqual(, self.revision)




