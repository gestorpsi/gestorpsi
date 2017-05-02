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

from gestorpsi.phone.models import PhoneType
from django.core.exceptions import ValidationError

class PhoneTypeTest(TestCase):

    def test_can_save_phone_type(self):
        phone_type = PhoneType(description = "My phone type")
        self.assertEqual(None, phone_type.save())

    def test_not_save_when_invalid_fields(self):
        phone_type = PhoneType()
        with self.assertRaisesRegex(ValidationError,'description'):
            phone_type.full_clean()
