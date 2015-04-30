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

from gestorpsi.client.models import Client
from gestorpsi.client.models import Person
# from gestorpsi.organization.models  import Organization

import unittest


class ClientTest(unittest.TestCase):
    def setUp(self):
        #		organization = Organization(name='Organizacao Teste',short_name='OT')
        person = Person(name='Levi Moraes')
        self.client = Client(person=person)
        self.active = True

    def testEmployeeReturn(self):
        self.assertEqual(self.client.person.name, 'Levi Moraes')

    def testIsActiveMethod(self):
        self.assertEqual(self.client.is_active(), True)

    def testListItemTitle(self):
        pass

    def testListItemTitleAditional(self):
        pass