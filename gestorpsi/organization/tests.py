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

from gestorpsi.phone.models import Phone, PhoneType
from gestorpsi.organization.models import Organization
from gestorpsi.internet.models import EmailType, Email
from django.test import Client
import unittest


class OrganizationTest(unittest.TestCase):
    def setUp(self):
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



