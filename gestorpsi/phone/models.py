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
from gestorpsi.util.uuid_field import UuidField

class PhoneType(models.Model):
    """
    This class was created to represent phone types. Each phone type has
    a short description.
    @author: Sergio Durand
    @version: 1.0
    @see: Phone
    """
    description = models.CharField(max_length=20)
    def __unicode__(self):
        return self.description

class Phone(models.Model):
    """
    This class holds information related to phone numbers.
    @author: Sergio Durand
    @version: 1.0
    @see: PhoneType
    """
    id= UuidField(primary_key=True)
    area = models.CharField(max_length=2)
    phoneNumber = models.CharField(max_length=8)
    ext = models.CharField(max_length=4, blank=True)
    phoneType = models.ForeignKey(PhoneType)
    # Generic Relationship
    content_type = models.ForeignKey(ContentType)
    object_id = models.CharField(max_length=36)
    content_object = generic.GenericForeignKey()

    def __cmp__(self, other):
        if (self.area == other.area) and \
           (self.phoneNumber == other.phoneNumber) and \
           (self.ext == other.ext) and \
           (self.phoneType == other.phoneType):
            return 0
        else:
            return 1
    
    def __unicode__(self):
        return "(%s) %s" % (self.area, self.phoneNumber)

reversion.register(Phone)
