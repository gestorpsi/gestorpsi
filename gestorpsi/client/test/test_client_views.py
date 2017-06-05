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
from django.test import Client as TestClient
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, UserManager, Group

from gestorpsi.client.models import Client, ClientManager
from gestorpsi.company.models import Company
from gestorpsi.client.models import Person
from gestorpsi.service.models import Service, ServiceType, Area
from gestorpsi.phone.models import Phone
from gestorpsi.admission.models import ReferralChoice as AdmissionChoice
from gestorpsi.organization.models import Organization
from gestorpsi.authentication.views import login_check
from gestorpsi.util.test_utils import *
from gestorpsi.util.test_utils import add_permission

from model_mommy import mommy

class ClientViewsTests(TestCase):
    def setUp(self):
        self.c = TestClient()
        setup_required_data()


    def test_unlogged_users_should_be_redirected(self):
        req = self.c.get(reverse('client-index'))
        self.assertEqual(req.status_code, 302)


    def test_admin_should_have_access_to_clients_page(self):
        # user creation and login
        self.c.post(reverse('registration-register'), user_stub())
        user = User.objects.get(username=user_stub()["username"])
        user.is_superuser = True
        user.save()
        add_permission(user, 'client_list')
        res = self.c.login(
            username=user.username, password=user_stub()["password1"]
        )
        req = self.c.get(reverse('client-index'))
        self.assertEqual(req.status_code, 200)


    def test_admin_should_be_able_to_add_cliente_with_valid_arguments(self):
        self.c.post(reverse('registration-register'), user_stub())
        setup_required_service()
        user = User.objects.get(username=user_stub()["username"])
        user.is_superuser = True
        user.save()
        add_permission(user, 'client_read')
        add_permission(user, 'client_list')
        self.c.login(
            username=user_stub()["username"], password=user_stub()["password1"]
        )
        old_client_count = Client.objects.count()
        r = self.c.get(reverse('client-form-new'))
        self.assertEqual(r.status_code, 200)
        self.c.post(reverse('client-form-save'), client_stub())
        new_client = Client.objects.all()[0]
        r = self.c.post(
            reverse('client-home', kwargs={'object_id': str(new_client.id)})
        )
        self.assertEqual(Client.objects.count(), old_client_count+1)
        self.assertEqual(r.status_code, 200)


    def test_client_should_not_create_with_none_arguments(self):
        self.c.post(reverse('registration-register'), user_stub())
        setup_required_service()
        self.c.login(
            username=user_stub()["username"], password=user_stub()["password1"]
        )
        user = User.objects.get(username=user_stub()["username"])
        user.is_superuser = True
        user.save()
        old_client_count = Client.objects.count()
        self.c.get(reverse('client-form-new'))
        self.c.get(reverse('client-form-save'))
        self.assertEqual(Client.objects.count(), old_client_count)


    def test_client_should_be_changed(self):
        self.c.post(reverse('registration-register'), user_stub())
        self.assertEqual(User.objects.all().count(), 1)
        user = User.objects.get(username=user_stub()["username"])
        user.is_superuser = True
        user.save()
        add_permission(user, 'client_write')
        add_permission(user, 'client_read')
        add_permission(user, 'client_list')
        self.c.login(
            username=user_stub()["username"], password=user_stub()["password1"]
        )
        setup_required_service()
        res = self.c.get(reverse('client-form-new'))
        self.assertEqual(res.status_code, 200)
        self.c.post(reverse('client-form-save'), client_stub())
        old_client_count = Client.objects.count()
        new_client = Client.objects.all()[0]
        form_args = {'object_id': str(new_client.id) }
        self.c.get(
            reverse('client-form-save', kwargs=form_args),
            change_client_stub()
        )
        change_client = Client.objects.all()[0]
        self.assertEqual(
            change_client.person.nickname, change_client_stub()["nickname"]
        )
        self.assertEqual(Client.objects.count(), old_client_count)


    def test_company_should_create_with_valid_arguments(self):
        self.c.post(reverse('registration-register'), user_stub())
        user = User.objects.get(username=user_stub()["username"])
        user.is_superuser = True
        add_permission(user, 'client_write')
        setup_required_service()
        setup_required_client()
        old_company_count = Company.objects.count()
        person = Person.objects.get(name='Pessoa')
        self.c.login(
            username=user_stub()["username"], password=user_stub()["password1"]
        )
        self.c.post(
            reverse('client-company-save'),
            {'person': person,
                'name': person.name,
                'nickname': person.nickname,
                'photo': 'foto',
                'gender': 2,
                'comments': ''
            }
        )
        self.assertEqual(Company.objects.count(), old_company_count+1)


    def test_company_should_create_with_none_arguments(self):
        self.c.post(reverse('registration-register'), user_stub())
        self.c.login(
            username=user_stub()["username"], password=user_stub()["password1"]
        )
        user = User.objects.get(username=user_stub()["username"])
        user.is_superuser = True
        user.save()
        setup_required_service()
        setup_required_client()
        old_company_count = Company.objects.count()
        self.c.get(reverse('client-company-save'))
        self.assertEqual(Company.objects.count(), old_company_count)
