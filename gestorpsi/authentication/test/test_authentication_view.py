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

from django.db import models
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from gestorpsi.util.test_utils import setup_required_data, bad_user_stub, user_stub

from model_mommy import mommy


class SignupTests(TestCase):
    def setUp(self):
        self.c = Client()

    def test_have_access_to_signup_page(self):
        response = self.c.get(reverse('registration-register'))
        self.assertEqual(response.status_code, 200)

    def test_signup_shouldnt_work_for_wrong_values(self):
        old_user_count = User.objects.count()
        response = self.c.post(reverse('registration-register'), bad_user_stub())
        self.assertEqual(User.objects.count(), old_user_count)

    def test_signup_with_correct_data_should_increase_total_number_of_users(self):
        mommy.make('address.State')
        city = mommy.make('address.City')
        mommy.make('gcm.Plan', staff_size=99, duration=1)
        mommy.make('address.Address', city=city)
        mommy.make('address.AddressType', description='Comercial')
        mommy.make('place.PlaceType', description='Matriz')
        mommy.make('gcm.PaymentType', pk=4)
        mommy.make('gcm.PaymentType', pk=1)
        phone_type = mommy.make('phone.PhoneType', description="comercial")
        phone = mommy.make('phone.Phone', area='23', phoneNumber='111111111', phoneType=phone_type)

        mommy.make('place.RoomType')
        mommy.make('document.TypeDocument', description='CPF')

        old_user_count = User.objects.count()
        response = self.c.post(reverse('registration-register'), user_stub())
        self.assertEqual(User.objects.count(), old_user_count+1)
        self.assertEqual(response.status_code, 200)
