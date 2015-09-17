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
        tobias = User
        joaquim = Person
        mcdonalds = Organization

        self.user = tobias
        self.organization = [mcdonalds]
        self.try_login = 10
        self.crypt_temp = "cryptografia"
        self.org_active = models.ForeignKey(
            mcdonalds, related_name="org_active", null=True)
        self.person = joaquim
        self.objects = UserManager()

        self.perfil = Profile
        self.perfil.user = self.user
        self.perfil.organization = self.organization
        self.perfil.try_login = self.try_login
        self.perfil.crypt_temp = self.crypt_temp
        self.perfil.org_active = self.org_active
        self.perfil.person = self.person
        self.perfil.objects = self.objects

    def test_user_is_set(self):
        self.assertTrue(issubclass(self.perfil.user, User))

    def test_user_parms_is_avaible(self):
        self.assertIsNotNone(self.perfil.user.pk)

    # def test_organization_is_set(self):
    #     self.assertIsInstance(
    #         self.perfil.organization, Organization)

    # def test_try_login_is_set(self):
    #     self.assertEquals(self.perfil.try_login, 10)

    # def test_crypt_temp_is_set(self):
    #     self.assertEquals(self.perfil.crypt_temp, "cryptografia")

    # def test_org_active_is_set(self):
    #     self.assertIsInstance(self.perfil.org_active, models.ForeignKey)

    # def test_person_is_set(self):
    #     self.assertIsInstance(self.perfil.person, models.OneToOneField)

    # def test_objects_is_set(self):
    #     self.assertIsInstance(self.perfil.objects, UserManager)


# class RoleTest(TestCase):

#     def setUp(self):
#         self.tobias = Group
#         self.joaquim = Profile
#         self.mcdonalds = Organization

#         self.papel = Role

#         self.papel.profile = models.ForeignKey(self.joaquim)
#         self.papel.organization = models.ForeignKey(self.mcdonalds)
#         self.papel.group = models.ForeignKey(self.tobias)

#     def test_profile_is_set(self):
#         self.assertIsInstance(self.papel.profile, models.ForeignKey)

#     def test_organization_is_set(self):
#         self.assertIsInstance(self.papel.organization, models.ForeignKey)

#     def test_group_is_set(self):
#         self.assertIsInstance(self.papel.group, models.ForeignKey)

#     def test_unicode(self):
#         saida = u"%s | %s | %s" % (self.joaquim, self.mcdonalds, self.tobias)
#         self.assertEquals(self.papel.__unicode__, saida)
