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

from gestorpsi.internet.models import EmailType, Email, Site, InstantMessenger
from gestorpsi.internet.models import IMNetwork
import unittest


class EmailTest(unittest.TestCase):

    def setUp(self):
        self.email = Email(email='test')
        emailWork = EmailType(description='Work')
        emailWork.save()
        self.email.emailType = emailWork
        self.email.object_id = 'test1'

        self.emailTest = Email(email='test')
        self.emailTest.emailType = emailWork
        self.emailTest.object_id = 'teste'

    def testCmp(self):
        self.assertEquals(cmp(self.email.email, self.emailTest.email), 0)
        self.assertEquals(cmp(self.email.emailType,
                              self.emailTest.emailType), 0)

    def testUnicode(self):
        self.assertEquals(self.email.email, unicode(self.emailTest.email))


class SiteTest(unittest.TestCase):

    def setUp(self):
        self.site = Site(description='Test', site='random site')
        self.anotherSite = Site(description='Test', site='random site')

    def testCmp(self):
        self.assertEquals(cmp(self.site.site, self.anotherSite.site), 0)
        self.assertEquals(cmp(self.site.description,
                              self.anotherSite.description), 0)

    def testUnicode(self):
        self.assertEquals(self.site.site, unicode(self.site.site))


class IMNetworkTest(unittest.TestCase):

    def setUp(self):
        self.IMNetwork = IMNetwork(description="Test Description")

    def testUnicode(self):
        self.assertEquals(self.IMNetwork.description,
                          unicode(self.IMNetwork.description))


class InstantMessengerTest(unittest.TestCase):

    def setUp(self):
        self.net = IMNetwork(description="Test Description")
        self.instant = InstantMessenger(identity='Test', network=self.net)
        self.instant2 = InstantMessenger(identity='Test', network=self.net)

    def testCmp(self):
        self.assertEquals(cmp(self.instant.identity,
                          self.instant2.identity), 0)
        self.assertEquals(cmp(self.instant.network,
                          self.instant2.network), 0)

    def testUnicode(self):
        self.assertEquals(self.instant.identity,
                          unicode(self.instant.identity))
