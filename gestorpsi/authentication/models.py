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

from django.db import models
from gestorpsi.organization.models import Organization
from django.contrib.auth.models import User, UserManager
from gestorpsi.util import CryptographicUtils as cryptoUtils

class Profile(models.Model):
    user = models.ForeignKey(User, unique=True)
    organization = models.ManyToManyField(Organization, null=True)
    try_login = models.IntegerField(default = 0, null=True)
    org_active = models.OneToOneField(Organization, related_name="org_active", null=True)
    
    objects = UserManager()


