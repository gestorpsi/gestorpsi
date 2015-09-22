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
from django.test import TestCase
from .models import Profile, Role


class ProfileTest(TestCase):

    def setUp(self):
        tobias = User()
        joaquim = Person()
        mcdonalds = Organization()
        papel = Role()

        self.perfil = Profile()
        self.perfil.user = tobias
        tobias.username = "Tobias"
        self.perfil.pk = 99
        mcdonalds.pk = 12
        joaquim.pk = 44
        self.perfil.org_active = mcdonalds
        self.perfil.person = joaquim
        self.perfil._set_temp("abacate")

    def test_user_is_set(self):
        self.assertIsInstance(self.perfil.user, User)

    def test_user_parms_are_avaible(self):
        self.assertIsNone(self.perfil.user.id)

    def test_organization_is_set(self):
        self.assertIsNotNone(self.perfil.organization)

    def test_try_login_is_set(self):
        self.assertFalse(self.perfil.try_login)

    def test_crypt_temp_is_set(self):
        self.assertIsNotNone(self.perfil.crypt_temp)

    def test_org_active_is_set(self):
        self.assertEquals(self.perfil.org_active_id, self.perfil.org_active.pk)

    def test_person_is_set(self):
        self.assertEquals(self.perfil.person_id, self.perfil.person.pk)

    def test_unicode(self):
        self.assertEquals(
            self.perfil.user.username, unicode(self.perfil))

    def test_set_temp(self):
        self.assertEquals(self.perfil.crypt_temp, "adf59a5eebcef0f8")

    def test_get_temp(self):
        self.assertEquals(self.perfil._get_temp(), "abacate")
