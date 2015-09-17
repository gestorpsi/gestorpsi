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
from django.contrib.auth.models import User, UserManager
from django.test import TestCase
from .models import Profile


class ProfileTest(TestCase):

    def setUp(self):
        tobias = User
        joaquim = Person
        mcdonalds = Organization

        self.user = models.OneToOneField(tobias)
        self.organization = models.ManyToManyField(
            mcdonalds, through='Role', null=True)
        self.try_login = models.IntegerField(default=0, null=True)
        self.crypt_temp = models.CharField(
            max_length=256, blank=True, null=True)
        self.org_active = models.ForeignKey(
            mcdonalds, related_name="org_active", null=True)
        self.person = models.OneToOneField(joaquim, null=True)
        self.objects = UserManager()

        self.profile = Profile
        self.profile.user = self.user
        self.profile.organization = self.organization
        self.profile.try_login = self.try_login
        self.profile.crypt_temp = self.crypt_temp
        self.profile.org_active = self.org_active
        self.profile.person = self.person
        self.profile.objects = self.objects

    def test_user_is_set(self):
        self.assertIsInstance(self.profile.user, models.OneToOneField)

    def test_organization_is_set(self):
        self.assertIsInstance(
            self.profile.organization, models.ManyToManyField)

    def test_try_login_is_set(self):
        self.assertIsInstance(self.profile.try_login, models.IntegerField)

    def test_crypt_temp_is_set(self):
        self.assertIsInstance(self.profile.crypt_temp, models.CharField)

    def test_org_active_is_set(self):
        self.assertIsInstance(self.profile.org_active, models.ForeignKey)

    def test_person_is_set(self):
        self.assertIsInstance(self.profile.person, models.OneToOneField)

    def test_objects_is_set(self):
        self.assertIsInstance(self.profile.objects, UserManager)
