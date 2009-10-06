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
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _
from gestorpsi.address.models import State
from gestorpsi.util.uuid_field import UuidField

DOCUMENT_TYPE = (
    (1, _('Person Document')),
    (2, _('Company Document')),
)

class Issuer(models.Model):
    description = models.CharField(max_length=100)
    def __unicode__(self):
        return u"%s" % self.description
    class Meta:
        ordering = ['description']

class TypeDocument(models.Model):
    description = models.CharField(max_length=30)
    source = models.IntegerField(choices=DOCUMENT_TYPE, default=1)
    def __unicode__(self):
        return u"%s" % (self.description)
    class Meta:
        ordering = ['description']

class Document(models.Model):
    id = UuidField(primary_key=True)
    typeDocument = models.ForeignKey(TypeDocument)
    document = models.CharField(max_length=20)
    issuer = models.ForeignKey(Issuer, null=True, blank=True)
    state = models.ForeignKey(State, null=True, blank=True)
    
    content_type = models.ForeignKey(ContentType)
    object_id = models.CharField( max_length=36 )
    content_object = generic.GenericForeignKey()
    
    def __cmp__(self, other):
        if (self.typeDocument == other.typeDocument) and \
           (self.document == other.document) and \
           (self.issuer == other.issuer) and \
           (self.state == other.state):
            return 0
        else:
            return 1

    def __unicode__(self):
        text = u"%s: %s" % (self.typeDocument, self.document)
        if self.issuer != None:
            text += u" %s" % self.issuer
        if self.state != None:
            text += u" %s" % self.state.shortName
        return text

