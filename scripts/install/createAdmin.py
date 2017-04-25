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

import sys, os

parent_dir = os.path.realpath(__file__  + '/../../')
sys.path.append(parent_dir)

import header

from django.contrib.auth.models import User
if User.objects.count() == 0:
    account_username = 'gestorpsi'
    account_password = '123456'

    print('\n\n')
    print('*****************************')
    print('Creating adminuser account')
    print('Username: ', account_username)
    print('Password: ', account_password)
    print('*****************************')

    admin = User.objects.create(username=account_username)
    admin.set_password(account_password)
    admin.is_superuser = True
    admin.is_staff = True
    admin.save()
