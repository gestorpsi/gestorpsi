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

from gestorpsi.client.models import Client, ClientManager
from gestorpsi.client.models import Person
from gestorpsi.phone.models import Phone
# from gestorpsi.organization.models  import Organization

import unittest


class ClientModelTest(unittest.TestCase):
    def setUp(self):
        #organization = Organization(name='Organizacao Teste',short_name='OT')
        person = Person()
        person.name = 'Levi Moraes'
        person.id = 01
        person.active = True

        phone = Phone()
        phone.phoneNumber = '12344321'

        #person.phones = phone

        self.client = Client()
        self.client.person = person

        self.client

    def testEmployeeReturn(self):
        self.assertEqual(self.client.person.name, 'Levi Moraes')

    def testIsActiveMethod(self):
        self.assertTrue(self.client.is_active())

    def testIsNotActive(self):
        pass

    def testListItemTitle(self):
        self.assertEqual(self.client.list_item_title(), 'Levi Moraes')

    def testIsActive(self):
        self.assertEqual(self.client.is_active(),True)

    def testListItemTitleAditional(self):
        self.assertEqual(self.client.list_item_title_aditional(),'')

    def testListItemDescription(self):
        self.assertEqual(self.client.list_item_description(),'')

    def tearDown(self):
        del self.client


class ClientViewTest():
    def setup(self):
        pass
