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
from .models import ReferralChoice, AdmissionManager, AdmissionInRangeManager, AdmissionReferral, Attach
from gestorpsi.organization.models import Organization
from datetime import datetime


class ReferralChoiceTest(TestCase):

    def setUp(self):
        self.referralchoice = ReferralChoice(
            description="Descricao", nick="Nick", weight=123, color="Color")
        self.description = "Descricao"
        self.nick = "Nick"
        self.weight = 123
        self.color = "Color"

    def testUnicode(self):
        self.assertEquals(self.description, unicode(self.referralchoice))
        self.assertEquals("Nick", self.nick)
        self.assertEquals(123, self.weight)
        self.assertEquals("Color", self.color)

    def testUnicodeFalse(self):
        self.assertNotEquals("False", unicode(self.referralchoice))


class AdmissionManagerTest(TestCase):

    def setUp(self):
        pass


class AdmissionInRangeManagerTest(TestCase):

    def setUp(self):
        pass


class AdmissionReferralTest(TestCase):

    def setUp(self):
        self.admissionreferral = AdmissionReferral(id=1,
                                                   signed_bythe_client=True,
                                                   date=datetime(2015, 9, 15,
                                                                 12, 12, 12))
        self.id = 11
        self.signed_bythe_client = False
        self.date = datetime(2015, 9, 15, 13, 13, 13)

    def testUnicode(self):
        self.assertEquals(11, self.id)
        self.assertEquals(False, self.signed_bythe_client)
        self.assertEquals(datetime(2015, 9, 15, 13, 13, 13), self.date)


class AttachTest(TestCase):

    def setUp(self):
        self.attach = Attach(filename="Filename", description="description",
                             date=datetime(2015, 9, 15, 12, 12, 12),
                             file="File", type="TY")
        self.filename = "filename"
        self.description = "Description"
        self.date = datetime(2015, 9, 15, 15, 15, 15)
        self.file = "File"
        self.type = "ty"

    def testUnicode(self):
        self.assertEquals(self.file, unicode(self.attach))
        self.assertEquals("Description", self.description)
        self.assertEquals(datetime(2015, 9, 15, 15, 15, 15), self.date)
        self.assertEquals("filename", self.filename)
        self.assertEquals("ty", self.type)
