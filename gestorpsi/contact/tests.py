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

from gestorpsi.contact.models import Contact
from django.test import TestCase


class TestContact(TestCase):
    def setUp(self):

        self.contact = Contact()

        self.contact.type = 1
        
    def testIs_organization(self):
        self.assertEquals(self.contact.is_organization(), True)
        
    def testIs_professional(self):
        self.assertEquals(self.contact.is_professional(), False)
