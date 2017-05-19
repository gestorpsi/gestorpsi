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
from gestorpsi.person.models import Person
from gestorpsi.organization.models import Organization
from django.contrib.auth.models import User, UserManager, Group
from django.contrib.sessions.models import Session
from django.test import TestCase
from gestorpsi.authentication.models import Profile, Role

from django.test import TestCase, Client, RequestFactory
from django.core.urlresolvers import reverse
from gestorpsi.util.test_utils import setup_required_data, bad_user_stub, user_stub


class SignupTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()

    def test_signup_should_work(self):
        response = self.client.get(reverse('registration-register'))
        self.assertEqual(response.status_code, 200)

    def test_signup_shouldnt_work_for_wrong_values(self):
        setup_required_data()
        old_user_count = User.objects.count()
        response = self.client.post(reverse('registration-register'), bad_user_stub())
        self.assertEqual(User.objects.count(), old_user_count)

    def test_signup_with_correct_data_should_increase_total_number_of_users(self):
        setup_required_data()
        old_user_count = User.objects.count()
        response = self.client.post(reverse('registration-register'), user_stub())
        self.assertEqual(User.objects.count(), old_user_count+1)
        self.assertEqual(response.status_code, 200)
