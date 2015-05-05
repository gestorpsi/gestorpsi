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
from gestorpsi.address.models import Country, State, City, Address, AddressType
from django.test import TestCase


class CountryTest(TestCase):
	def setUp(self):
		self.country = Country(name="Brasil")
		self.name = "Brasil"

	def testUnicode(self):
		self.assertEquals(self.name, unicode(self.country))


class StateTest(TestCase):
	def setUp(self):
		self.state = State(name="Goias")
		self.name = "Goias"

	def testUnicode(self):
		self.assertEquals(self.name, unicode(self.state))


class CityTest(TestCase):
	def setUp(self):
		self.city = City(name="Taguatinga")
		self.name = "Taguatinga"

	def testUnicode(self):
		self.assertEquals(self.name, unicode(self.city))


class AddressTypeTest(TestCase):
	def setUp(self):
		self.address_type = AddressType(description="Quadra 1")
		self.description = "Quadra 1"

	def testUnicode(self):
		self.assertEquals(self.description, unicode(self.address_type))


class AddressTest(TestCase):
	def setUp(self):
		self.city = City(name="Taguatinga")
		self.address_type = AddressType(description="Quadra 1")
		self.address = Address(addressPrefix="DF",addressLine1="Quadra 2",addressNumber="24",
			addressLine2="Quadra 3",zipCode="72241302",neighborhood="bairro tal",city=self.city,
			address_type=self.address_type)
		self.addressPrefix="DF"
		self.addressLine1 = "Quadra 2"
		self.addressNumber = "24"
		self.addressLine2 = "Quadra 3"
		self.zipCode = "72241302"
		self.neighborhood = "bairro tal"

	def testUnicode(self):
#		expected_result = "%s %s %s %s<br />%s %s %s %s %s (%s)" % (self.addressPrefix, self.addressLine1, self.addressNumber, self.addressLine2, self.zipCode, self.neighborhood, self.city, '' if not hasattr(self.city, 'state') else self.city.state.shortName, '' if not hasattr(self.city, 'state') else self.city.state.country, self.addressType)
		expected_result = "erro"
        self.assertEquals(expected_result, unicode(self.address))
