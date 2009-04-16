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

"""

INSTALL:

1) ./manage.py syncdb

2) Create a user with SIGN UP option in Login Page

3) execute install2.py

export PYTHONPATH=<directory from your project>
python install2.py

"""

from os import environ
environ['DJANGO_SETTINGS_MODULE'] = 'gestorpsi.settings'
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Group, Permission, User

user = User.objects.get(pk=2)
appnames = ['client', 'contacts', 'place', 'schedule', 'employee', 'professional', 'service', 'device', 'organization']
for appname in appnames:
    ct, created = ContentType.objects.get_or_create(model='', app_label=appname, defaults={'name': appname})
    user.user_permissions.add(Permission.objects.create(codename='%s_list' % appname, name='%s List' % appname.capitalize(), content_type=ct))
    user.user_permissions.add(Permission.objects.create(codename='%s_read' % appname, name='%s Read' % appname.capitalize(), content_type=ct))
    user.user_permissions.add(Permission.objects.create(codename='%s_write' % appname, name='%s Write' % appname.capitalize(), content_type=ct))

print "Done!"
