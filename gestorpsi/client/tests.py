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
from django.test import TestCase, RequestFactory
from django.test import Client as Cl
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
from gestorpsi.util.test_utils import client_stub, user_stub, setup_required_data, setup_required_service, setup_required_client

class ClientTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        # OBS: Using cl instead of client to evade conflicts with Client class
        self.client = Cl()
        setup_required_data()
        self.name_client = 'Cliente 10'

    def test_client_index_should_redirect_unlogged_user(self):
        req = self.client.get(reverse('client-index'))
        self.assertEqual(req.status_code, 302)

    def test_client_index_should_work_for_logged_user(self):
        # user creation and login
        self.client.post(reverse('registration-register'), user_stub())
        res = self.client.login(username=user_stub()["username"], password=user_stub()["password1"])
        user = User.objects.get(username=user_stub()["username"])
        user.is_superuser = True
        user.save()
        req = self.client.get(reverse('client-index'))
        self.assertEqual(req.status_code, 200)

    def test_client_should_create_with_valid_arguments(self):
        self.client.post(reverse('registration-register'), user_stub())
        self.client.login(username=user_stub()["username"], password=user_stub()["password1"])
        user = User.objects.get(username=user_stub()["username"])
        user.is_superuser = True
        user.save()

        setup_required_service()
        old_client_count = Client.objects.count()

        self.client.post(reverse('client-form-new'))
        self.client.post(reverse('client-form-save'), client_stub())

        new_client = Client.objects.all()[0]

        new_client_response = self.client.get(reverse('client-home', kwargs={'object_id': str(new_client.id)}))

        self.assertEqual(Client.objects.count(), old_client_count+1)
        self.assertEqual(new_client_response.status_code, 200)

    def test_client_should_not_create_with_none_arguments(self):
        self.client.post(reverse('registration-register'), user_stub())
        self.client.login(username=user_stub()["username"], password=user_stub()["password1"])
        user = User.objects.get(username=user_stub()["username"])
        user.is_superuser = True
        user.save()

        setup_required_service()
        old_client_count = Client.objects.count()

        self.client.post(reverse('client-form-new'))
        self.client.post(reverse('client-form-save'))

        self.assertEqual(Client.objects.count(), old_client_count)

    def test_company_should_create_with_valid_arguments(self):
        self.client.post(reverse('registration-register'), user_stub())
        self.client.login(username=user_stub()["username"], password=user_stub()["password1"])
        user = User.objects.get(username=user_stub()["username"])
        user.is_superuser = True
        user.save()

        setup_required_service()
        setup_required_client()

        old_company_count = Company.objects.count()

        person = Person.objects.get(name='Pessoa')

        self.client.post(reverse('client-company-save'), {'person': person, 'name': person.name, 'nickname': person.nickname, 'photo': 'foto', 'gender': 2, 'comments': ''})
        
        self.assertEqual(Company.objects.count(), old_company_count+1)


    def test_company_should_create_with_none_arguments(self):
        self.client.post(reverse('registration-register'), user_stub())
        self.client.login(username=user_stub()["username"], password=user_stub()["password1"])
        user = User.objects.get(username=user_stub()["username"])
        user.is_superuser = True
        user.save()

        setup_required_service()
        setup_required_client()

        old_company_count = Company.objects.count()

        self.client.post(reverse('client-company-save'))
        
        self.assertEqual(Company.objects.count(), old_company_count)

class ClientModelTest(TestCase):
    def setUp(self):
        #organization = Organization(name='Organizacao Teste',short_name='OT')
        person = Person()
        person.name = 'Levi Moraes'
        person.id = 01
        person.active = True

        phone = Phone()
        phone.phoneNumber = '12344321'

        #person.phones = phone

        self.client = Client()
        self.client.person = person

        self.client

    def testEmployeeReturn(self):
        self.assertEqual(self.client.person.name, 'Levi Moraes')

    def testIsActiveMethod(self):
        self.assertTrue(self.client.is_active())

    def testIsNotActive(self):
        pass

    def testListItemTitle(self):
        self.assertEqual(self.client.list_item_title(), 'Levi Moraes')

    def testIsActive(self):
        self.assertEqual(self.client.is_active(),True)

    def testListItemTitleAditional(self):
        self.assertEqual(self.client.list_item_title_aditional(),'')

    def testListItemDescription(self):
        self.assertEqual(self.client.list_item_description(),'')

    def tearDown(self):
        del self.client

