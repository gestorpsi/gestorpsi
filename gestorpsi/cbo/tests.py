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

from django.test import TestCase
from .models import Occupation


class OccupationTest(TestCase):

    def setUp(self):
        self.occupation = Occupation(id=1,
                                     cbo_code="cbo_code", title="title")

        self.id = 1
        self.cbo_code = "cbo_code"
        self.title = "title"

    def testUnicode(self):
        self.assertEquals(self.title, unicode(self.occupation))
        self.assertEquals(1, self.id)
        self.assertEquals("cbo_code", self.cbo_code)
