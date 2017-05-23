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
from gestorpsi.place.models import PlaceType, Place
from gestorpsi.address.models import City, State, Country, AddressType
import unittest

from django.test import TestCase, RequestFactory
from django.test import Client as Cl
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from gestorpsi.util.test_utils import client_stub, user_stub, setup_required_data, setup_required_service, setup_required_client

class PlaceTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        # OBS: Using cl instead of client to evade conflicts with Client class
        self.client = Cl()
        setup_required_data()
        self.name_client = 'Cliente 10'

    def test_client_index_should_redirect_unlogged_user(self):
        req = self.client.get(reverse('client-index'))
        self.assertEqual(req.status_code, 302)

    def test_client_index_should_work_for_logged_user(self):
        # user creation and login
        self.client.post(reverse('registration-register'), user_stub())
        res = self.client.login(username=user_stub()["username"], password=user_stub()["password1"])
        user = User.objects.get(username=user_stub()["username"])
        user.is_superuser = True
        user.save()
        req = self.client.get(reverse('client-index'))
        self.assertEqual(req.status_code, 200)

    def test_show_list_of_places(self):
        self.client.post(reverse('registration-register'), user_stub())
        res = self.client.login(username=user_stub()["username"], password=user_stub()["password1"])
        user = User.objects.get(username=user_stub()["username"])
        user.is_superuser = True
        user.save()
        response= self.client.get('/place/')
        self.assertEquals(200,response.status_code)
        self.assertTemplateUsed(response, 'place/place_list.html')

    def test_not_show_list_for_unlogged_user(self):
        self.client.logout() # guarantee that the given user is signed out
        response= self.client.get('/place/')
        self.assertEquals(302,response.status_code)

    def test_show_place_add_form(self):
        self.client.post(reverse('registration-register'), user_stub())
        res = self.client.login(username=user_stub()["username"], password=user_stub()["password1"])
        user = User.objects.get(username=user_stub()["username"])
        user.is_superuser = True
        user.save()
        response= self.client.get('/place/add/')
        self.assertEquals(200,response.status_code)
        self.assertTemplateUsed(response, 'place/place_form.html')

    def test_not_show_form_for_unlogged_user(self):
        self.client.logout() # guarantee that the given user is signed out
        response= self.client.get('/place/add/')
        self.assertEquals(302,response.status_code)

    def test_show_deactive_places(self):
        self.client.post(reverse('registration-register'), user_stub())
        res = self.client.login(username=user_stub()["username"], password=user_stub()["password1"])
        user = User.objects.get(username=user_stub()["username"])
        user.is_superuser = True
        user.save()
        response= self.client.get('/place/deactive/')
        self.assertEquals(200,response.status_code)
        self.assertTemplateUsed(response, 'place/place_list.html')

    def test_not_show_deactive_places_for_unlogged_user(self):
        self.client.logout() # guarantee that the given user is signed out
        response= self.client.get('/place/deactive/')
        self.assertEquals(302,response.status_code)

    # Foi possível obter o label e o id mas não acessar a rota
    # def test_show_place(self):
    #     self.client.post(reverse('registration-register'), user_stub())
    #     res = self.client.login(username=user_stub()["username"], password=user_stub()["password1"])
    #     user = User.objects.get(username=user_stub()["username"])
    #     user.is_superuser = True
    #     user.save()
    #     place = Place.objects.get(label='testing place')
    #     print place.label + ' id: ' + place.id
    #     response= self.client.get('/place/'+place.id+'/')
    #     self.assertEquals(200,response.status_code)
    #     self.assertTemplateUsed(response, 'place/place_form.html')

'''
class UnitPlaceTest(unittest.TestCase):
    def setUp(self):
        self.place= Place(label='testing place')
        place_type= PlaceType(description= 'a place type')
        place_type.save()
        self.place.place_type= place_type
        phone_type= PhoneType(description= 'phone type test')
        phone= Phone(area= '23', phoneNumber= '45679078', ext= '4444', phoneType= phone_type)
        phone.content_object = self.place

        addressType=AddressType(description='Home')
        addressType.save()
        address = Address()
        address.addressPrefix = 'Rua'
        address.addressLine1 = 'Rui Barbosa, 1234'
        address.addressLine2 = 'Anexo II - Sala 4'
        address.neighborhood = 'Centro'
        address.zipCode = '12345-123'
        address.addressType = AddressType.objects.get(pk=1)

        country= Country( name= 'test', nationality= 'testing' )
        country.save()
        state= State(name= 'test', shortName= 't', country= country )
        state.save()
        city= City(name= 'test', state= state)
        city.save()

        address.city = city
        address.content_object = self.place

        self.place.save()

    def testDefaultPlace(self):
        #get all places stored in the database and put them in a list
        #then compare the first (and probably only) stored-place with self.place
        self.assertEquals(  Place.objects.all()[0], self.place, 'place has not been appropriately saved' )
'''
class ViewPlaceTest( unittest.TestCase ):
    urls = 'gestorpsi.place.urls'

    def setUp(self):
        print 'setup'

    def testIndex(self):
        #c= Client()
        #print "%s" % c.post( '/index/', { 'joaoajoa': 2 } )
        #self.assertEquals( 200, response.status_code )
        pass

    def tearDown(self):
        print 'teardown'
