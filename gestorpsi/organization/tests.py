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
from django.contrib.auth.models import User, UserManager, Group
from gestorpsi.person.models import Person
from gestorpsi.phone.models import Phone, PhoneType
from gestorpsi.organization.models import Organization
from gestorpsi.internet.models import EmailType, Email
from django.test.client import Client
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test import Client as Cl
from django.test import TestCase
from gestorpsi.util.test_utils import user_stub, setup_required_data

class OrganizationModelTest(TestCase):
    def setUp(self):
    	self.name= 'testing organization'
        self.organization = Organization(name='testing organization')

    def testGetFisrtPhoneFull(self):
    	self.phone_type = PhoneType(description='phone type test')
        self.phone_type.save()
        self.phone = Phone(area='23', phoneNumber='45679078', ext='4444',
                      phoneType=self.phone_type, content_object = self.organization)
        self.phone.save()

        self.assertEquals(self.organization.get_first_phone(), self.phone)
    def testGetFisrtPhoneEmpty(self):
        self.assertEquals(self.organization.get_first_phone(), '')

    def testGetFisrtEmailFull(self):
    	self.email_type = EmailType(description='type email')
    	self.email_type.save()
    	self.email= Email(email='vinirmv@gmail.com',email_type= self.email_type, content_object=self.organization)
    	self.email.save()
    	self.assertEquals(self.organization.get_first_email(), self.email)

    def testGetFisrtEmailEmpty(self):
        self.assertEquals(self.organization.get_first_email(), '')

    def testUnicode(self):
    	self.assertEquals(self.name, unicode(self.organization))

    def testClientNotExist(self):
    	self.assertFalse(self.organization.clients().exists())
    	#self.assertQuerysetEqual(self.organization.clients(), [])

class OrganizationViewTest(TestCase):
    def setUp(self):
        # OBS: Using cl instead of client to evade conflicts with Client class
        self.cl = Cl()
        setup_required_data()

    def testShowFormOnGet(self):
        self.client.post(reverse('registration-register'), user_stub())
        res = self.client.login(username=user_stub()["username"], password=user_stub()["password1"])
        user = User.objects.get(username=user_stub()["username"])
        user.is_superuser = True
        user.save()
        response= self.client.get('/organization/')
        self.assertEquals(200,response.status_code)
        self.assertTemplateUsed(response, 'organization/organization_form.html')

    def testNotShowFormOnGet(self):
        self.client.logout() # guarantee that the given user is signed out
        response= self.client.get('/organization/')
        self.assertEquals(302,response.status_code)

    def testShowFormResultsOnPost(self):
        self.client.post(reverse('registration-register'), user_stub())
        res = self.client.login(username=user_stub()["username"], password=user_stub()["password1"])
        user = User.objects.get(username=user_stub()["username"])
        user.is_superuser = True
        user.save()
        response= self.client.post('/organization/', trade_name="Change trade name test", name="Change name company")
        self.assertEquals(200,response.status_code)

    def testShowSignatureOnGet(self):
        self.client.post(reverse('registration-register'), user_stub())
        res = self.client.login(username=user_stub()["username"], password=user_stub()["password1"])
        user = User.objects.get(username=user_stub()["username"])
        user.is_superuser = True
        user.save()
        response= self.client.post(reverse('organization-signature'))
        self.assertEquals(200,response.status_code)
        self.assertTemplateUsed(response, 'organization/organization_signature.html')

    def testNotShowSignatureOnGet(self):
        self.client.logout() # guarantee that the given user is signed out
        response= self.client.get(reverse('organization-signature'))
        self.assertEquals(302,response.status_code)

    def testShowSuspensionOnGet(self):
        self.client.post(reverse('registration-register'), user_stub())
        res = self.client.login(username=user_stub()["username"], password=user_stub()["password1"])
        user = User.objects.get(username=user_stub()["username"])
        user.is_superuser = True
        user.save()
        response= self.client.post(reverse('organization-suspension'))
        self.assertEquals(200,response.status_code)
        self.assertTemplateUsed(response, 'organization/organization_signature_suspension.html')

    def testNotShowSuspensionOnGet(self):
        self.client.logout() # guarantee that the given user is signed out
        response= self.client.get(reverse('organization-suspension'))
        self.assertEquals(302,response.status_code)
