#!/usr/bin/env python
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

import sys
sys.path.append('..')

import header

from django.contrib.auth.models import User
if User.objects.count() == 0:
    admin = User.objects.create(username='gestorpsi')
    admin.set_password('123456')
    admin.is_superuser = True
    admin.is_staff = True
    admin.save()
