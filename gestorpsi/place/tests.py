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

from gestorpsi.address.models import Address
from gestorpsi.phone.models import Phone, PhoneType
from gestorpsi.place.models import PlaceType, Place, RoomType
from gestorpsi.address.models import City, State, Country, AddressType, Address
from django.core.urlresolvers import reverse
from gestorpsi.contact.models import Contact
from django.test import Client
import unittest
from gestorpsi.gcm.models.plan import *
from gestorpsi.gcm.models.payment import *
from gestorpsi.document.models import *


class PlaceTest(unittest.TestCase):
    def setUp(self):
        self.place = Place(label='testing place')
        
        if len(PlaceType.objects.all())==0:
            place_type = PlaceType(description='Matriz')
            place_type.save()
            document = TypeDocument(description='CPF')
            document.save()
            a = AddressType(description='Comercial')
            a.save()
            room_type = RoomType()
            room_type.description = 'sala test'
            room_type.save()
            plan = Plan()
            plan.name = 'Teste 1'
            plan.value = 324.00
            plan.duration = 1
            plan.staff_size = 1
            plan.save()
            p = PaymentType()
            p.id = 1
            p.name = 'Teste 1'
            p.save()
            p  = PaymentType()
            p.id = 4
            p.name = 'Teste 4'
            p.save()
            country = Country(name='test', nationality='testing')
            country.save()
            state = State(name='test', shortName='t', country=country)
            state.save()
            city = City(name='test', state=state)
            city.save()
        else:
            place_type = PlaceType.objects.get(description='Matriz')
        self.place.place_type = place_type
        phone_type = PhoneType(description='phone type test')
        phone_type.save()
        self.phone = Phone(area='23', phoneNumber='45679078', ext='4444',
                      phoneType=phone_type)
        self.phone.content_object = self.place
        addressType = AddressType(description='Home')
        addressType.save()
        address = Address()
        address.addressPrefix = 'Rua'
        address.addressLine1 = 'Rui Barbosa, 1234'
        address.addressLine2 = 'Anexo II - Sala 4'
        address.neighborhood = 'Centro'
        address.zipCode = '12345-123'
        address.addressType = AddressType.objects.get(pk=1)

        country = Country(name='test', nationality='testing')
        country.save()
        state = State(name='test', shortName='t', country=country)
        state.save()
        city = City(name='test', state=state)
        city.save()

        address.city = city
        address.content_object = self.place

        self.place.save()
        
        

    def testTypeReturnHoursWork(self):
        self.assertEquals(type(self.place.hours_work()), type([]))


    def testReturnHoursWork(self):
        self.assertEquals(self.place.hours_work(), [07, 00, 12.0])

    def testGetFisrtPhone(self):
        self.assertEquals(self.place.get_first_phone(), '')

    def testInvalidFirst(self):
        pass

    def testoccurrences(self):
        self.assertEquals(self.place.occurrences(),[])

    def testDefaultPlace(self):
        #get all places stored in the database and put them in a list
        #then compare the first (and probably only) stored-place
        #with self.place
        self.assertEquals(Place.objects.all()[0], self.place,
                          'place has not been appropriately saved')


class ViewPlaceTest(unittest.TestCase):
    urls = 'gestorpsi.place.urls'

    def setUp(self):
        #print 'setup'
        pass

    def testLogin(self):
        c=Client()
        #print "%s" % c.post( '/index/', { 'joaoajoa': 2 } )
        responseR = c.post('/accounts/register/',{"username":u'usermane',"city":u'1',"password2":u'password',"name":u'asd',"address_number":u'111',"password1":u'password',"zipcode":u'11111-111',"cpf":u'111.111.111-11',"phone":u'(11) 1111-11111',"state":u'1',"plan":u'1',"address":u'1111',"organization":u'asd',"shortname":u'asd',"email":u'asd@asd.com'})
        #print "%s " % responseR
        self.assertEquals( 302, responseR.status_code )
        response = c.post('/accounts/authentication/',{"username":u'usermane',"password":u'password'})
        #print "%s " % response
        self.assertEquals( 302, response.status_code )
        #response = c.post('/contact/')
        #print "%s " % response
        #self.assertEquals(200,response.status_code)
        pass

    def tearDown(self):
        #print 'teardown'
        pass


def suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(PlaceTest)
    suite.addTest(ViewPlaceTest('testLogin'))
    return suite
