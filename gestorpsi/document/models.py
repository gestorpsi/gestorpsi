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
from gestorpsi.address.models import State
from gestorpsi.util import audittrail
from gestorpsi.util.uuid_field import UuidField
from gestorpsi.util import CryptographicUtils as cryptoUtils

class Issuer(models.Model):
    description = models.CharField(max_length=30)
    def __unicode__(self):
        return u"%s" % self.description

class TypeDocument(models.Model):
    description = models.CharField(max_length=30)
    def __unicode__(self):
        return u"%s" % self.description

class Document(models.Model):
    id = UuidField(primary_key=True)
    typeDocument = models.ForeignKey(TypeDocument)
    crypt_document = models.CharField(max_length=96)
    issuer = models.ForeignKey(Issuer, null=True, blank=True)
    state = models.ForeignKey(State, null=True, blank=True)
    
    #Generic Relationship
    content_type = models.ForeignKey(ContentType)
    object_id = models.CharField( max_length=36 )
    content_object = generic.GenericForeignKey()
    
    def _set_document(self, value):
        self.crypt_document= cryptoUtils.encrypt_attrib( value )
        
    def _get_document(self):
        return cryptoUtils.decrypt_attrib( self.crypt_document )
    
    document= property( _get_document, _set_document )
    
    history = audittrail.AuditTrail()

    def __cmp__(self, other):
        if (self.typeDocument == other.typeDocument) and \
           (self.document == other.document) and \
           (self.issuer == other.issuer) and \
           (self.state == other.state):
            return 0
        else:
            return 1

    def __unicode__(self):
        return u"%s: %s / %s - %s" % (self.typeDocument, self.document, self.issuer, self.state)
