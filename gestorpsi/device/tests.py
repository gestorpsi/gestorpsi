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
from gestorpsi.util.test_utils import setup_required_data

class DeviceTest(TestCase):
	def setUp(self):
		self.factory = RequestFactory()
		self.cl = Cl()
		setup_required_data()

	def test_device_index_should_redirect_to_device_list(self):
		req = self.cl.get(reverse('device-index'))
		self.assertEqual(req.status_code, 302)