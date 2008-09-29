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
from gestorpsi.util import audittrail
from gestorpsi.util.uuid_field import UuidField
from gestorpsi.util import CryptographicUtils as cryptoUtils

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
    crypt_area = models.CharField(max_length=16)
    crypt_phoneNumber = models.CharField(max_length=32)
    crypt_ext = models.CharField(max_length=16, blank=True)
    phoneType = models.ForeignKey(PhoneType)
    # Generic Relationship
    content_type = models.ForeignKey(ContentType)
    object_id = models.CharField(max_length=36)
    content_object = generic.GenericForeignKey()
    
    history= audittrail.AuditTrail()
    
    def _set_area(self, value):
        self.crypt_area= cryptoUtils.encrypt_attrib( value )
        
    def _get_area(self):
        return cryptoUtils.decrypt_attrib( self.crypt_area )
    
    def _set_phoneNumber(self, value):
        self.crypt_phoneNumber= cryptoUtils.encrypt_attrib( value )
        
    def _get_phoneNumber(self):
        return cryptoUtils.decrypt_attrib( self.crypt_phoneNumber )
    
    def _set_ext(self, value):
        self.crypt_ext= cryptoUtils.encrypt_attrib( value )
        
    def _get_ext(self):
        return cryptoUtils.decrypt_attrib( self.crypt_ext )
    
    area= property( _get_area, _set_area )
    phoneNumber= property( _get_phoneNumber, _set_phoneNumber )
    ext= property( _get_ext, _set_ext )
    
    def __cmp__(self, other):
        if (self.area == other.area) and \
           (self.phoneNumber == other.phoneNumber) and \
           (self.ext == other.ext) and \
           (self.phoneType == other.phoneType):
            return 0
        else:
            return 1
    
    def __unicode__(self):
        """
        Returns a representation of this phone number as a unicode C{string}; this C{string} follows the pattern:
        I{(area) phone-number}.
        """
        return "(%s) %s" % (self.area, self.phoneNumber)
