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

class EmailType(models.Model):
    description= models.CharField(max_length=45)
    def __unicode__(self):
        return self.description
    class Meta:
        ordering = ['description']

class Email(models.Model):
    id = UuidField(primary_key= True)
    email = models.CharField(max_length=100, blank=True)
    email_type = models.ForeignKey(EmailType)
    notify = models.BooleanField(default=False)
    
    # Generic Relation
    content_type = models.ForeignKey(ContentType)
    object_id = models.CharField(max_length=36)
    content_object = generic.GenericForeignKey()

    def __cmp__(self, other):
        if (self.email == other.email) and \
           (self.email_type == other.email_type):
            return 0
        else:
            return 1

    def __unicode__(self):
        return self.email

    def revision(self):
        return reversion.get_for_object(self).order_by('-revision__date_created').latest('revision__date_created').revision

reversion.register(Email)

class Site(models.Model):
    id = UuidField(primary_key=True)
    description = models.CharField(max_length=100, blank=True)
    site = models.CharField(max_length=100, blank=True)

    # Generic Relation
    content_type = models.ForeignKey(ContentType)
    object_id = models.CharField(max_length=36)
    content_object = generic.GenericForeignKey()

    def __cmp__(self, other):
        if (self.description == other.description) and \
           (self.site == other.site):
            return 0
        else:
            return 1    
    
    def __unicode__(self):
        return self.site

    def revision(self):
        return reversion.get_for_object(self).order_by('-revision__date_created').latest('revision__date_created').revision

reversion.register(Site)

class IMNetwork(models.Model):
    description = models.CharField(max_length=30)
    def __unicode__(self):
        return self.description
    class Meta:
        ordering = ['description']

class InstantMessenger(models.Model):
    id = UuidField(primary_key=True)
    identity = models.CharField(max_length=100, blank=True)
    network = models.ForeignKey(IMNetwork, blank=True)

    # Generic Relation
    content_type = models.ForeignKey(ContentType)
    object_id = models.CharField(max_length=36)
    content_object = generic.GenericForeignKey()

    def __cmp__(self, other):
        if (self.identity == other.identity) and \
           (self.network == other.network):
            return 0
        else:
            return 1

    def __unicode__(self):
        return "%s (%s)" % (self.identity, self.network)

    def revision(self):
        return reversion.get_for_object(self).order_by('-revision__date_created').latest('revision__date_created').revision

reversion.register(InstantMessenger)
