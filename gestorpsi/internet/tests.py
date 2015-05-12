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
from gestorpsi.internet.views import email_list
from django.test import TestCase


class EmailTest(TestCase):

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


    def testEmptyEmailList(self):
        expected_result = email_list([],[],[])
        self.assertListEqual(expected_result, [])

'''
>For future improvement 

    def testOneEmailInList(self):
        id = ["1312"]
        email = [self.email]
        email_typeId = [self.email.emailType.id]
        
        expected_result = email_list(id, email, email_typeId)

        email = Email(id=id[0],
                      email=email[0],
                      email_type=EmailType.objects.get(pk=emailTypeId[0]))

        self.assertIsNotNone(expected_result)
        self.assertEquals(len(expected_result), 1)
        self.assertIsInstance(expected_result[0], Email)
        self.assertIn(email, expected_result) 
'''

class SiteTest(TestCase):

    def setUp(self):
        self.site = Site(description='Test', site='random site')
        self.anotherSite = Site(description='Test', site='random site')

    def testCmp(self):
        self.assertEquals(cmp(self.site.site, self.anotherSite.site), 0)
        self.assertEquals(cmp(self.site.description,
                              self.anotherSite.description), 0)

    def testUnicode(self):
        self.assertEquals(self.site.site, unicode(self.site.site))


class IMNetworkTest(TestCase):

    def setUp(self):
        self.IMNetwork = IMNetwork(description="Test Description")

    def testUnicode(self):
        self.assertEquals(self.IMNetwork.description,
                          unicode(self.IMNetwork.description))


class InstantMessengerTest(TestCase):

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
