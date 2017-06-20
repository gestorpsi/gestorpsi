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
from gestorpsi.place.models import PlaceType, Place, Room, RoomType
from gestorpsi.address.models import City, State, Country, AddressType
import unittest

from django.test import TestCase, RequestFactory
from django.test import Client as Cl
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from gestorpsi.util.test_utils import user_stub, setup_required_data, place_stub, room_stub

class PlaceTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        # OBS: Using cl instead of client to evade conflicts with Client class
        self.client = Cl()
        setup_required_data()

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

    def test_show_add_place(self):
        self.client.post(reverse('registration-register'), user_stub())
        res = self.client.login(username=user_stub()["username"], password=user_stub()["password1"])
        user = User.objects.get(username=user_stub()["username"])
        user.is_superuser = True
        user.save()

        old_place_count = Place.objects.count()
        response= self.client.post('/place/save/', place_stub())

        new_place = Place.objects.all()[0]
        new_place_response =  self.client.get('/place/'+str(new_place.id)+'/')
        self.assertEquals(200,new_place_response.status_code)
        self.assertEquals(Place.objects.count(), old_place_count+1)

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

    def test_show_add_room(self):
        self.client.post(reverse('registration-register'), user_stub())
        res = self.client.login(username=user_stub()["username"], password=user_stub()["password1"])
        user = User.objects.get(username=user_stub()["username"])
        user.is_superuser = True
        user.save()

        old_room_count = Room.objects.count()
        print old_room_count
        response= self.client.post('/place/room/save/', room_stub())
        print response
        new_room = Room.objects.all()[0]
        new_room_response =  self.client.get('/place/room/'+str(new_room.id)+'/')
        self.assertEquals(200,new_room_response.status_code)
        self.assertEquals(Room.objects.count(), old_room_count+1)
