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

from django.test import TestCase, Client, RequestFactory
from django.core.urlresolvers import reverse
from gestorpsi.util.test_utils import setup_required_data, bad_user_stub, user_stub


class UsersViewsTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()

    def test_users_index_work_for_signed_users(self):
        setup_required_data()
        response = self.client.post(reverse('registration-register'), user_stub())
        response = self.client.get(reverse('user-index'))
        self.assertEqual(response.status_code, 200)
