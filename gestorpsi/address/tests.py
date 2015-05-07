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
        country = Country(name='test', nationality='testing')
        country.save()
        state = State(name='test', shortName='t', country=country)
        state.save()
        city = City(name='test', state=state)
        city.save()
        self.city = city

        address_type = AddressType(description="Quadra 1",weight=3)
        address_type.save()
        self.address_type = address_type

        self.address = Address(addressPrefix="DF", addressLine1="Quadra 2",
                               addressNumber="24", addressLine2="Quadra 3",
                               zipCode="72241302", neighborhood="bairro tal",
                               city=self.city, addressType=self.address_type)
        self.addressPrefix="DF"
        self.addressLine1 = "Quadra 2"
        self.addressNumber = "24"
        self.addressLine2 = "Quadra 3"
        self.zipCode = "72241302"
        self.neighborhood = "bairro tal"

    def testUnicode(self):
        #expected_result = "" + self.address.addressPrefix + " " + self.address.addressLine1 + " " + self.address.addressNumber + " " + self.address.addressLine2 + " " + self.address.zipCode + " " + self.address.neighborhood
        expected_result = u"%s %s %s %s<br />%s %s %s %s %s (%s)" % (\
            self.address.addressPrefix, self.address.addressLine1, self.address.addressNumber, self.address.addressLine2, \
            self.address.zipCode, self.address.neighborhood, self.address.city, '' if not hasattr(self.address.city, 'state') else self.address.city.state.shortName, '' if not hasattr(self.address.city, 'state') else self.address.city.state.country, self.address.addressType\
        )
        self.assertEquals(expected_result, unicode(self.address))