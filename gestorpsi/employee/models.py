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

import reversion
from django.db import models
from gestorpsi.person.models import Person
from gestorpsi.util.uuid_field import UuidField

class EmployeeManager(models.Manager):
    def active(self, organization):
        return super(EmployeeManager, self).get_query_set().filter(active=True, person__organization = organization).order_by('person__name')
    def deactive(self, organization):
        return super(EmployeeManager, self).get_query_set().filter(active=False, person__organization = organization).order_by('person__name')

class Employee(models.Model):
    id= UuidField(primary_key=True)
    person = models.OneToOneField(Person)
    hiredate = models.DateField(blank=True, null=True)
    job = models.CharField(max_length=30, blank=True)
    active = models.BooleanField(default=True)
    objects = EmployeeManager()
    
    def __unicode__(self):
        return u"%s" % self.person.name

    class Meta:
        ordering = ['person']    

    def revision(self):
        return reversion.models.Version.objects.get_for_object(self).order_by('-revision__date_created').latest('revision__date_created').revision

reversion.register(Employee, follow=['person'])


