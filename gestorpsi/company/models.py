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
from django.utils.translation import ugettext_lazy as _

from gestorpsi.client.models import Client
from gestorpsi.person.models import Person
from gestorpsi.util.models import Cnae


COMPANY_SIZE = (
    (1, _('Small')),
    (2, _('Medium')),
    (3, _('Big')),
)

class Company(models.Model):
    client = models.ManyToManyField(Client, blank=True, through='CompanyClient') # employees of company
    person = models.OneToOneField(Person, blank=True, null=True)
    size = models.IntegerField(_('Company Size'), blank=True, null=True, choices=COMPANY_SIZE)
    cnae_class = models.CharField(_('CNAE Subclass Code'), blank=True, null=True, max_length=9)

    def __unicode__(self):
        return u'%s' % self.person.name
    
    def _cnae_class_name(self):
        c = Cnae.objects.filter(id=self.cnae_class)
        if len(c):
            return c[0].cnae_class
        return None
    cnae_class_name = property(_cnae_class_name)


class CompanyClient(models.Model):
    client = models.ForeignKey(Client) # employees of company
    company = models.ForeignKey(Company)
    responsible = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return u'%s' % (self.client)

    class Meta:
        ordering = ['-active', '-responsible', 'client']
        unique_together = (('client', 'company'),)
