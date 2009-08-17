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

2) python install2.py

3) Sign up a new user in login page

"""

import sys
sys.path.append('..')

from os import environ
environ['DJANGO_SETTINGS_MODULE'] = 'gestorpsi.settings'
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Group, Permission, User

appnames = ['admission', 'client', 'contact', 'place', 'schedule', 'employee', 'careprofessional', 'service', 'device', 'organization', 'users', 'referral', 'upload']
for appname in appnames:
    ct, created = ContentType.objects.get_or_create(model='', app_label=appname, defaults={'name': appname})
    Permission.objects.get_or_create(codename='%s_list' % appname, name='%s List' % appname.capitalize(), content_type=ct)
    Permission.objects.get_or_create(codename='%s_read' % appname, name='%s Read' % appname.capitalize(), content_type=ct)
    Permission.objects.get_or_create(codename='%s_write' % appname, name='%s Write' % appname.capitalize(), content_type=ct)

# Administrator
grp_administrator,created = Group.objects.get_or_create(name='administrator')
grp_administrator.permissions.add(Permission.objects.get(codename='admission_write'))
grp_administrator.permissions.add(Permission.objects.get(codename='admission_read'))
grp_administrator.permissions.add(Permission.objects.get(codename='admission_list'))
grp_administrator.permissions.add(Permission.objects.get(codename='users_write'))
grp_administrator.permissions.add(Permission.objects.get(codename='users_read'))
grp_administrator.permissions.add(Permission.objects.get(codename='users_list'))
grp_administrator.permissions.add(Permission.objects.get(codename='client_write'))
grp_administrator.permissions.add(Permission.objects.get(codename='client_read'))
grp_administrator.permissions.add(Permission.objects.get(codename='client_list'))
grp_administrator.permissions.add(Permission.objects.get(codename='referral_write'))
grp_administrator.permissions.add(Permission.objects.get(codename='referral_read'))
grp_administrator.permissions.add(Permission.objects.get(codename='referral_list'))
grp_administrator.permissions.add(Permission.objects.get(codename='schedule_write'))
grp_administrator.permissions.add(Permission.objects.get(codename='schedule_read'))
grp_administrator.permissions.add(Permission.objects.get(codename='schedule_list'))
grp_administrator.permissions.add(Permission.objects.get(codename='contact_write'))
grp_administrator.permissions.add(Permission.objects.get(codename='contact_read'))
grp_administrator.permissions.add(Permission.objects.get(codename='contact_list'))
grp_administrator.permissions.add(Permission.objects.get(codename='device_write'))
grp_administrator.permissions.add(Permission.objects.get(codename='device_read'))
grp_administrator.permissions.add(Permission.objects.get(codename='device_list'))
grp_administrator.permissions.add(Permission.objects.get(codename='employee_write'))
grp_administrator.permissions.add(Permission.objects.get(codename='employee_read'))
grp_administrator.permissions.add(Permission.objects.get(codename='employee_list'))
grp_administrator.permissions.add(Permission.objects.get(codename='organization_write'))
grp_administrator.permissions.add(Permission.objects.get(codename='organization_read'))
grp_administrator.permissions.add(Permission.objects.get(codename='organization_list'))
grp_administrator.permissions.add(Permission.objects.get(codename='place_write'))
grp_administrator.permissions.add(Permission.objects.get(codename='place_read'))
grp_administrator.permissions.add(Permission.objects.get(codename='place_list'))
grp_administrator.permissions.add(Permission.objects.get(codename='careprofessional_write'))
grp_administrator.permissions.add(Permission.objects.get(codename='careprofessional_read'))
grp_administrator.permissions.add(Permission.objects.get(codename='careprofessional_list'))
grp_administrator.permissions.add(Permission.objects.get(codename='service_write'))
grp_administrator.permissions.add(Permission.objects.get(codename='service_read'))
grp_administrator.permissions.add(Permission.objects.get(codename='service_list'))
grp_administrator.permissions.add(Permission.objects.get(codename='upload_write'))
grp_administrator.permissions.add(Permission.objects.get(codename='upload_read'))
grp_administrator.permissions.add(Permission.objects.get(codename='upload_list'))

# Professional
grp_professional, created = Group.objects.get_or_create(name='professional')
grp_professional.permissions.add(Permission.objects.get(codename='client_read'))
grp_professional.permissions.add(Permission.objects.get(codename='client_list'))
grp_professional.permissions.add(Permission.objects.get(codename='schedule_write'))
grp_professional.permissions.add(Permission.objects.get(codename='schedule_read'))
grp_professional.permissions.add(Permission.objects.get(codename='schedule_list'))
grp_professional.permissions.add(Permission.objects.get(codename='contact_write'))
grp_professional.permissions.add(Permission.objects.get(codename='contact_read'))
grp_professional.permissions.add(Permission.objects.get(codename='contact_list'))
grp_professional.permissions.add(Permission.objects.get(codename='device_read'))
grp_professional.permissions.add(Permission.objects.get(codename='device_list'))
grp_professional.permissions.add(Permission.objects.get(codename='employee_list'))
grp_professional.permissions.add(Permission.objects.get(codename='careprofessional_write'))
grp_professional.permissions.add(Permission.objects.get(codename='careprofessional_read'))
grp_professional.permissions.add(Permission.objects.get(codename='careprofessional_list'))
grp_professional.permissions.add(Permission.objects.get(codename='referral_write'))
grp_professional.permissions.add(Permission.objects.get(codename='referral_read'))
grp_professional.permissions.add(Permission.objects.get(codename='referral_list'))
grp_professional.permissions.add(Permission.objects.get(codename='service_read'))
grp_professional.permissions.add(Permission.objects.get(codename='service_list'))
grp_administrator.permissions.add(Permission.objects.get(codename='upload_write'))
grp_administrator.permissions.add(Permission.objects.get(codename='upload_read'))
grp_administrator.permissions.add(Permission.objects.get(codename='upload_list'))

# Secretary
grp_secretary, created = Group.objects.get_or_create(name='secretary')
grp_administrator.permissions.add(Permission.objects.get(codename='admission_write'))
grp_administrator.permissions.add(Permission.objects.get(codename='admission_read'))
grp_administrator.permissions.add(Permission.objects.get(codename='admission_list'))
grp_administrator.permissions.add(Permission.objects.get(codename='users_write'))
grp_administrator.permissions.add(Permission.objects.get(codename='users_read'))
grp_administrator.permissions.add(Permission.objects.get(codename='users_list'))
grp_secretary.permissions.add(Permission.objects.get(codename='client_write'))
grp_secretary.permissions.add(Permission.objects.get(codename='client_read'))
grp_secretary.permissions.add(Permission.objects.get(codename='client_list'))
grp_secretary.permissions.add(Permission.objects.get(codename='referral_write'))
grp_secretary.permissions.add(Permission.objects.get(codename='referral_read'))
grp_secretary.permissions.add(Permission.objects.get(codename='referral_list'))
grp_secretary.permissions.add(Permission.objects.get(codename='schedule_write'))
grp_secretary.permissions.add(Permission.objects.get(codename='schedule_read'))
grp_secretary.permissions.add(Permission.objects.get(codename='schedule_list'))
grp_secretary.permissions.add(Permission.objects.get(codename='contact_read'))
grp_secretary.permissions.add(Permission.objects.get(codename='contact_list'))
grp_secretary.permissions.add(Permission.objects.get(codename='employee_list'))
grp_secretary.permissions.add(Permission.objects.get(codename='careprofessional_read'))
grp_secretary.permissions.add(Permission.objects.get(codename='careprofessional_list'))
grp_administrator.permissions.add(Permission.objects.get(codename='upload_write'))
grp_administrator.permissions.add(Permission.objects.get(codename='upload_read'))
grp_administrator.permissions.add(Permission.objects.get(codename='upload_list'))

# Client
grp_client, created = Group.objects.get_or_create(name='client')
grp_client.permissions.add(Permission.objects.get(codename='client_read'))

print "Done!"
