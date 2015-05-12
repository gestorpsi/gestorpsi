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

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User
from gestorpsi.person.models import Person
from gestorpsi.phone.models import Phone, PhoneType
from gestorpsi.phone.views import is_equal, phone_delete
from gestorpsi.organization.models import Organization
from gestorpsi.internet.models import EmailType, Email
from django.test.client import Client
from django.test import TestCase, RequestFactory
import unittest

class testPhoneView(unittest.TestCase):
	def setUp(self):
		self.organization = Organization(name='testing organization')
		self.phone_type=PhoneType(description= 'description phone')
		self.phone_type.save()
		self.phone= Phone(area='21', phoneNumber='11111111',ext='111', 
			phoneType= self.phone_type, content_object = self.organization)
		self.phone.save()
	
	def testIfPhoneIsEqual(self):
		expected=is_equal(self.phone)
		self.assertEqual(expected, True)
		self.assertTrue(is_equal(self.phone))

	def testIfPhoneIsDeleting(self):
		phone= Phone(area='21', phoneNumber='0',ext='111', 
			phoneType= self.phone_type, content_object = self.organization)
		self.phone.save()
		self.assertIsNone(phone_delete(phone.id, phone.phoneNumber))
