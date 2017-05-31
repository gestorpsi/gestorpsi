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

from gestorpsi.client.models import Client, ClientManager
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db.utils import DatabaseError
from model_mommy import mommy

class ClientModelTest(TestCase):
    def test_can_save_client_with_min_attributes(self):
        fake_user = mommy.make('auth.User')
        fake_person = mommy.make('person.Person', user=fake_user)

        old_count = Client.objects.count() 

        client = Client()
        client.person = fake_person
        client.idRecord = 42
        client.save()
        self.assertGreater(Client.objects.count(), old_count)

    def test_raise_exception_when_missing_fields(self):
        fake_user = mommy.make('auth.User')
        fake_person = mommy.make('person.Person', user=fake_user)

        client = Client()
        with self.assertRaisesMessage(DatabaseError, "person_id"):
            client.save()

        client.person = fake_person
        with self.assertRaisesMessage(DatabaseError, "idRecord"):
            client.save()
