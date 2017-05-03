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
from django.test import TestCase
from django.test import Client as Cl
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, UserManager, Group

from gestorpsi.client.models import Client, ClientManager
from gestorpsi.client.models import Person
from gestorpsi.phone.models import Phone
from gestorpsi.util.test_utils import user_stub, setup_required_data

class ClientTests(TestCase):
    def setUp(self):
        # OBS: Using cl instead of client to evade conflicts with Client class
        self.cl = Cl()
        setup_required_data()

    def test_client_index_should_redirect_unlogged_user(self):
        req = self.cl.get(reverse('client-index'))
        self.assertEqual(req.status_code, 302)

    def test_client_index_should_work_for_logged_user(self):
        # user creation and login
        self.cl.post(reverse('registration-register'), user_stub())
        self.cl.login(
            username=user_stub()["username"],
            password=user_stub()["password1"]
        )
        user = User.objects.get(username=user_stub()["username"])
        user.is_superuser = True
        user.save()
        req = self.cl.get(reverse('client-index'))
        self.assertEqual(req.status_code, 200)

