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
from gestorpsi.person.models import Person
from gestorpsi.admission.models import Referral, Indication
from gestorpsi.util.uuid_field import UuidField
from gestorpsi.util import CryptographicUtils as cryptoUtils
from gestorpsi.util import audittrail

class Relation(models.Model):
    description = models.CharField(max_length=30)
    def __unicode__(self):
        return u"%s" % self.description

class PersonLink(models.Model):
    person = models.OneToOneField(Person)
    relation = models.ForeignKey(Relation)
    responsible = models.BooleanField(default=False)
    def __unicode__(self):
        return u"%s" % self.person.firstName

CLIENT_STATUS = ( ('0','Inativo'),('1','Ativo'))
class Client(models.Model):
    id= UuidField( primary_key= True )
    person = models.OneToOneField(Person)
    crypt_idRecord = models.CharField(max_length=250)
    crypt_legacyRecord = models.CharField(max_length=250)
    crypt_healthDocument = models.CharField(max_length=250)
    admission_date = models.DateField(null=True)
    referral_choice = models.ForeignKey(Referral, null=True)
    indication_choice = models.ForeignKey(Indication, null=True)
    clientStatus = models.CharField(max_length=1, default = '1', choices=CLIENT_STATUS)
    person_link = models.ManyToManyField(PersonLink)
    comments = models.TextField(blank=True)
    history= audittrail.AuditTrail()

    def _get_idRecord(self):
        return cryptoUtils.decrypt_attrib( self.crypt_idRecord )
    
    def _set_idRecord(self, value):
        self.crypt_idRecord= cryptoUtils.encrypt_attrib( value )
    
    def _get_legacyRecord(self):
        return cryptoUtils.decrypt_attrib( self.crypt_legacyRecord )
    
    def _set_legacyRecord(self, value):
        self.crypt_legacyRecord= cryptoUtils.encrypt_attrib( value )
    
    def _get_healthDocument(self):
        return cryptoUtils.decrypt_attrib( self.crypt_healthDocument )
    
    def _set_healthDocument(self, value):
        self.crypt_healthDocument= cryptoUtils.encrypt_attrib( value )
    
    idRecord= property( _get_idRecord, _set_idRecord )
    legacyRecord= property( _get_legacyRecord, _set_legacyRecord )
    healthDocument= property( _get_healthDocument, _set_healthDocument )
    
    def __unicode__(self):
        return u"%s" % self.person.name
    
    class Meta:
        ordering = ['person']
