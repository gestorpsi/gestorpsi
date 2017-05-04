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
from django.contrib.auth.models import User
from gestorpsi.person.models import Person
from gestorpsi.phone.models import Phone, PhoneType
from gestorpsi.organization.models import Organization
from gestorpsi.internet.models import EmailType, Email
from django.test.client import Client
from django.test import TestCase
from django.core.urlresolvers import reverse



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

    '''
    def testClientExist(self):
    	User.objects.create(username="user1", password="password")
        user = User.objects.get(username="user1")
        Person.objects.create(user_id=user.id)
        self.person = Person.objects.get(user_id=user.id)
    	self.assertEqual(Tag.objects.get_for_object(Person.objects.get(pk=1).count(), 1)
    '''
class OrganizationViewTest(TestCase):
	def setUp(self):

		self.client=Client()
		response = self.client.post('/accounts/login/?next=/', {'username': 'user15', 'password': 'nicepass123'})

	def testShowFormOnGet(self):
		#self.client.login(username='user15', password ='nicepass123')
		response= self.client.get(reverse('organization-signature'))
		#print(response)
		self.assertEquals(200,response.status_code)
		#self.assertTemplateUsed(response, 'organization_signature.html')
