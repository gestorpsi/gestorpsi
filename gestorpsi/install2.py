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

2) execute install2.py

export PYTHONPATH=<directory from your project>
python install2.py

) Sign up a new user in login page

"""

from os import environ
environ['DJANGO_SETTINGS_MODULE'] = 'gestorpsi.settings'
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Group, Permission, User

appnames = ['client', 'contacts', 'place', 'schedule', 'employee', 'professional', 'service', 'device', 'organization']
for appname in appnames:
    ct, created = ContentType.objects.get_or_create(model='', app_label=appname, defaults={'name': appname})
    Permission.objects.create(codename='%s_list' % appname, name='%s List' % appname.capitalize(), content_type=ct)
    Permission.objects.create(codename='%s_read' % appname, name='%s Read' % appname.capitalize(), content_type=ct)
    Permission.objects.create(codename='%s_write' % appname, name='%s Write' % appname.capitalize(), content_type=ct)

# Administrator
grp_administrator = Group.objects.create(name='administrator')
grp_administrator.permissions.add(Permission.objects.get(codename='client_write'))
grp_administrator.permissions.add(Permission.objects.get(codename='client_read'))
grp_administrator.permissions.add(Permission.objects.get(codename='client_list'))
grp_administrator.permissions.add(Permission.objects.get(codename='schedule_write'))
grp_administrator.permissions.add(Permission.objects.get(codename='schedule_read'))
grp_administrator.permissions.add(Permission.objects.get(codename='schedule_list'))
grp_administrator.permissions.add(Permission.objects.get(codename='contacts_write'))
grp_administrator.permissions.add(Permission.objects.get(codename='contacts_read'))
grp_administrator.permissions.add(Permission.objects.get(codename='contacts_list'))
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
grp_administrator.permissions.add(Permission.objects.get(codename='professional_write'))
grp_administrator.permissions.add(Permission.objects.get(codename='professional_read'))
grp_administrator.permissions.add(Permission.objects.get(codename='professional_list'))
grp_administrator.permissions.add(Permission.objects.get(codename='service_write'))
grp_administrator.permissions.add(Permission.objects.get(codename='service_read'))
grp_administrator.permissions.add(Permission.objects.get(codename='service_list'))

# Psychologist
grp_psychologist = Group.objects.create(name='psychologist')
grp_psychologist.permissions.add(Permission.objects.get(codename='client_read'))
grp_psychologist.permissions.add(Permission.objects.get(codename='client_list'))
grp_psychologist.permissions.add(Permission.objects.get(codename='schedule_write'))
grp_psychologist.permissions.add(Permission.objects.get(codename='schedule_read'))
grp_psychologist.permissions.add(Permission.objects.get(codename='schedule_list'))
grp_psychologist.permissions.add(Permission.objects.get(codename='contacts_write'))
grp_psychologist.permissions.add(Permission.objects.get(codename='contacts_read'))
grp_psychologist.permissions.add(Permission.objects.get(codename='contacts_list'))
grp_psychologist.permissions.add(Permission.objects.get(codename='device_read'))
grp_psychologist.permissions.add(Permission.objects.get(codename='device_list'))
grp_psychologist.permissions.add(Permission.objects.get(codename='employee_list'))
grp_psychologist.permissions.add(Permission.objects.get(codename='professional_write'))
grp_psychologist.permissions.add(Permission.objects.get(codename='professional_read'))
grp_psychologist.permissions.add(Permission.objects.get(codename='professional_list'))
grp_psychologist.permissions.add(Permission.objects.get(codename='service_read'))
grp_psychologist.permissions.add(Permission.objects.get(codename='service_list'))

# Secretary
grp_secretary = Group.objects.create(name='secretary')
grp_secretary.permissions.add(Permission.objects.get(codename='client_write'))
grp_secretary.permissions.add(Permission.objects.get(codename='client_read'))
grp_secretary.permissions.add(Permission.objects.get(codename='client_list'))
grp_secretary.permissions.add(Permission.objects.get(codename='schedule_write'))
grp_secretary.permissions.add(Permission.objects.get(codename='schedule_read'))
grp_secretary.permissions.add(Permission.objects.get(codename='schedule_list'))
grp_secretary.permissions.add(Permission.objects.get(codename='contacts_read'))
grp_secretary.permissions.add(Permission.objects.get(codename='contacts_list'))
grp_secretary.permissions.add(Permission.objects.get(codename='employee_list'))
grp_secretary.permissions.add(Permission.objects.get(codename='professional_read'))
grp_secretary.permissions.add(Permission.objects.get(codename='professional_list'))

# Client
grp_client = Group.objects.create(name='client')
grp_client.permissions.add(Permission.objects.get(codename='client_read'))
grp_client.permissions.add(Permission.objects.get(codename='client_list'))
grp_client.permissions.add(Permission.objects.get(codename='schedule_read'))
grp_client.permissions.add(Permission.objects.get(codename='schedule_list'))


print "Done!"
