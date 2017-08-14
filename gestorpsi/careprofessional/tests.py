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

from django.test import TestCase, Client
from django.contrib.auth.models import User, UserManager, Group
from django.core.urlresolvers import reverse

from gestorpsi.util.test_utils import user_stub, setup_required_data, student_stub, change_student_stub
from gestorpsi.service.models import Area, ServiceType, Service
from gestorpsi.person.models import Person
from gestorpsi.careprofessional.models import CareProfessional


class StudentsTests(TestCase):
    def setUp(self):
        self.client = Client()
        setup_required_data()
        self.forbidden_string = "Desculpe-nos, mas você não tem permissão para executar essa operação."

    def test_student_should_show_forbidden_page_for_users_without_permission(self):
        self.client.post(reverse('registration-register'), user_stub())
        self.client.login(username=user_stub()["username"], password=user_stub()["password1"])
        response = self.client.get(reverse('student_index'))
        self.assertEqual(self.forbidden_string in response.content, True)

    def test_student_should_work_for_logged_users(self):
        self.client.post(reverse('registration-register'), user_stub())
        self.client.login(username=user_stub()["username"], password=user_stub()["password1"])
        user = User.objects.get(username=user_stub()["username"])
        user.is_superuser = True
        user.save()
        response = self.client.get(reverse('student_index'))
        self.assertEqual(self.forbidden_string in response.content, False)

    def test_student_should_be_created(self):
        self.client.post(reverse('registration-register'), user_stub())
        self.client.login(username=user_stub()["username"], password=user_stub()["password1"])
        user = User.objects.get(username=user_stub()["username"])
        user.is_superuser = True
        user.save()

        old_student_count = CareProfessional.objects.count()
        self.client.post(reverse('student_save'), student_stub())
        new_student = CareProfessional.objects.all()[0]
        new_student_response = self.client.get(reverse('student-form', kwargs={'object_id': str(new_student.id)}))

        self.assertEqual(CareProfessional.objects.count(), old_student_count + 1)
        self.assertEqual(new_student_response.status_code, 200)

    def test_student_should_not_create_with_none_arguments(self):
        self.client.post(reverse('registration-register'), user_stub())
        self.client.login(username=user_stub()["username"], password=user_stub()["password1"])
        user = User.objects.get(username=user_stub()["username"])
        user.is_superuser = True
        user.save()

        old_student_count = CareProfessional.objects.count()
        self.client.post(reverse('student_add'))

        self.assertEqual(CareProfessional.objects.count(), old_student_count)

    def test_student_should_be_changed(self):
        self.client.post(reverse('registration-register'), user_stub())
        self.client.login(username=user_stub()["username"], password=user_stub()["password1"])
        user = User.objects.get(username=user_stub()["username"])
        user.is_superuser = True
        user.save()

        self.client.post(reverse('student_save'), student_stub())
        old_student_count = CareProfessional.objects.count()

        new_student = CareProfessional.objects.all()[0]
        self.client.post(reverse('careprofessional-save-update', kwargs={'object_id': str(new_student.id)}),
                         change_student_stub())
        change_student = CareProfessional.objects.all()[0]
        change_student_response = self.client.get(reverse('student-form', kwargs={'object_id': str(new_student.id)}))

        self.assertEqual(change_student.person.name, change_student_stub()["name"])
        self.assertEqual(CareProfessional.objects.count(), old_student_count)
        self.assertEqual(change_student_response.status_code, 200)

    def test_student_should_be_deactivate(self):
        self.client.post(reverse('registration-register'), user_stub())
        self.client.login(username=user_stub()["username"], password=user_stub()["password1"])
        user = User.objects.get(username=user_stub()["username"])
        user.is_superuser = True
        user.save()

        self.client.post(reverse('student_save'), student_stub())
        old_student_count = CareProfessional.objects.count()

        new_student = CareProfessional.objects.all()[0]
        self.client.post(reverse('professional_order', kwargs={'object_id': str(new_student.id)}))
        change_student = CareProfessional.objects.all()[0]

        self.assertEqual(CareProfessional.objects.count(), old_student_count)
        self.assertEqual(change_student.active, False)
