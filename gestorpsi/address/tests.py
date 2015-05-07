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


from .models import Country, State, City, Address, AddressType
from .views import address_list


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


class AddressViewTest(TestCase):
    def setUp(self):
        self.country = Country(name='test', nationality='testing')
        self.country.save()
        self.state = State(name='test', shortName='t', country=self.country)
        self.state.save()
        self.city = City(name='test', state=self.state)
        self.city.save()
        self.address_type = AddressType(description="Quadra 1")
        self.address_type.save()

    def testEmptyAddressList(self):
        expected_result = address_list([],[],[], [], [], [], [], [],
                                       [], [], [], [])
        self.assertListEqual(expected_result, [])

    def testOneAddressInAddressList(self):
        id = ["12345"]
        addressPrefix = ["Prefix"]
        addressLine1 = ["addressLine1"]
        addressLine2 = ["addressLine2"]
        addressNumbers = [123]
        neighborhoods = ["DSAD"]
        zipCodes = ["72000-000"]
        addressTypeIds = [self.address_type.id]
        cityIds = [self.city.id]
        countryIds =  [self.country.id]
        foreignCityChars = [""]
        foreignStateChars = [""]

        expected_result = address_list(id, addressPrefix, addressLine1, addressLine2,
                                       addressNumbers, neighborhoods, zipCodes,
                                       addressTypeIds, cityIds, countryIds,
                                       foreignCityChars, foreignStateChars)

        address = Address(id=id[0], addressPrefix=addressPrefix[0],
                          addressLine1=addressLine1[0],
                          addressLine2=addressLine2[0],
                          addressNumber=addressNumbers[0],
                          neighborhood=neighborhoods[0],
                          zipCode=zipCodes[0],
                          addressType=AddressType.objects.get(pk=addressTypeIds[0]),
                          city=City.objects.get(pk=cityIds[0]))

        self.assertIsNotNone(expected_result)
        self.assertEquals(len(expected_result), 1)
        self.assertIsInstance(expected_result[0], Address)
        self.assertIn(address, expected_result)

