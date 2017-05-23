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
from gestorpsi.device.models import Device
from django.contrib.auth.models import User, UserManager, Group
from django.core.urlresolvers import reverse
from gestorpsi.util.test_utils import setup_required_data, user_stub

device_stub = {
	'device_brand': 'brand',
	'device_model': 'model',
	'device_part_number': 'part_number',
	'device_lendable': 'True',
	'device_comments': 'comments',
	'device_durability': '1',
	'device_prof_restriction': 'True',
	'device_mobility': '1',
	'device_active': 'True',
}

class DeviceTest(TestCase):
	def setUp(self):
		self.factory = RequestFactory()
		self.cl = Cl()
		setup_required_data()
		self.forbidden_string = "We're sorry, but you dont have permissions to execute this operation."

	def test_device_should_redirect_unlogged_users(self):
		self.cl.logout() 
		response = self.cl.get(reverse('device-index'))
		self.assertEqual(response.status_code, 302)

	def test_device_should_show_forbidden_page_for_users_without_permission(self):
		self.cl.post(reverse('registration-register'), user_stub())
		res = self.cl.login(username=user_stub()["username"], password=user_stub()["password1"])
		response = self.cl.get(reverse('device-index'))
		self.assertEqual(self.forbidden_string in response.content, True)

	def test_device_should_work_for_logged_users(self):
		self.cl.post(reverse('registration-register'), user_stub())
		res = self.cl.login(username=user_stub()["username"], password=user_stub()["password1"])
		user = User.objects.get(username=user_stub()["username"])
		user.is_superuser = True
		user.save()
		req = self.cl.get(reverse('device-index'))
		self.assertEqual(req.status_code, 200)

	def test_device_show_list_of_devices(self):
		self.cl.post(reverse('registration-register'), user_stub())
		res = self.cl.login(username=user_stub()["username"], password=user_stub()["password1"])
		user = User.objects.get(username=user_stub()["username"])
		user.is_superuser = True
		user.save()
		response= self.cl.get('/device/')

		self.assertEquals(200,response.status_code)
		self.assertTemplateUsed(response, 'device/device_list.html')

	def test_device_should_not_show_list_of_devices(self):
		self.client.logout()
		response= self.cl.get('/device/')

		self.assertEquals(302,response.status_code)

	def test_service_creation_should_work_for_correct_values(self):
		self.cl.post(reverse('registration-register'), user_stub())
		res = self.cl.login(username=user_stub()["username"], password=user_stub()["password1"])
		user = User.objects.get(username=user_stub()["username"])
		user.is_superuser = True
		user.save()
		device_count = Device.objects.all().count()

		self.device.post(reverse('device/device_form.html'))
		self.device.post(reverse('device.device_write'), device_stub())

		device_current_count = Device.objects.all().count()

		self.assertEqual(device_current_count, device_count+1)