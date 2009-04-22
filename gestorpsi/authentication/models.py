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
from gestorpsi.person.models import Person
from django.contrib.auth.models import User, UserManager

class Profile(models.Model):
    user = models.OneToOneField(User, unique=True)
    organization = models.ManyToManyField(Organization, null=True)
    try_login = models.IntegerField(default = 0, null=True)
    org_active = models.ForeignKey(Organization, related_name="org_active", null=True)
    person = models.OneToOneField(Person, null=True)
    
    objects = UserManager()

    def __unicode__(self):
        return u"%s" % self.user.username


