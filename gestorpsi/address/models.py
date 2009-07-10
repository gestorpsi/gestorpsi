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
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from gestorpsi.util import audittrail
from gestorpsi.util.uuid_field import UuidField

class Country(models.Model):
    name = models.CharField(max_length=50)
    nationality = models.CharField(max_length=50)
    def __unicode__(self):
        return u"%s" % self.name
    class Meta:
        ordering = ['name']

class State(models.Model):
    name = models.CharField(max_length=50)
    shortName = models.CharField(max_length=2)
    country = models.ForeignKey(Country)
    def __unicode__(self):
        return u"%s" % self.name
    class Meta:
        ordering = ['name']

class City(models.Model):
    ibge_code = models.CharField(max_length=10)
    name = models.CharField(max_length=50)
    state = models.ForeignKey(State)
    def __unicode__(self):
        return u"%s" % (self.name)
    class Meta:
        ordering = ['name']

class AddressType(models.Model):
    description = models.CharField(max_length=20)
    def __unicode__(self):
        return u"%s" % self.description

    class Meta:
        ordering = ['description']

class Address(models.Model):
    # Brazil Address
    id= UuidField( primary_key= True )
    addressPrefix = models.CharField(max_length=10)
    addressLine1 = models.CharField(max_length=50, blank=True)
    addressLine2 = models.CharField(max_length=50, blank=True)
    addressNumber = models.CharField(max_length=10, blank=True)
    neighborhood = models.CharField(max_length=30, blank=True)
    zipCode = models.CharField(max_length=10, blank=True)
    addressType = models.ForeignKey(AddressType)
    city = models.ForeignKey(City, null=True)
    # Foreign Address
    foreignCountry = models.ForeignKey(Country, null=True)
    foreignState   = models.CharField(max_length=20, blank=True)
    foreignCity    = models.CharField(max_length=50, blank=True)
    # Generic Relationship
    content_type = models.ForeignKey(ContentType)
    object_id = models.CharField(max_length=36)
    content_object = generic.GenericForeignKey()
    
    def __cmp__(self, other):
        if (self.addressPrefix == other.addressPrefix) and \
           (self.addressLine1 == other.addressLine1) and \
           (self.addressLine2 == other.addressLine2) and \
           (self.addressNumber == other.addressNumber) and \
           (self.neighborhood == other.neighborhood) and \
           (self.zipCode == other.zipCode) and \
           (self.addressType == other.addressType) and \
           (self.city == other.city) and \
           (self.foreignCountry == other.foreignCountry) and \
           (self.foreignState == other.foreignState) and \
           (self.foreignCity == other.foreignCity):
            return 0
        else:
            return 1    
    
    def __unicode__(self):
        return u"%s %s\n%s" % (self.addressPrefix, self.addressLine1, self.addressLine2)

    def revision(self):
        return reversion.models.Version.objects.get_for_object(self).order_by('-revision__date_created').latest('revision__date_created').revision

reversion.register(Address)
