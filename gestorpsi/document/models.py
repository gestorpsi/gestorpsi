# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from gestorpsi.address.models import State
from django.contrib import admin
from gestorpsi.util import audittrail
from gestorpsi.util.uuid_field import UuidField
from gestorpsi.util import CryptographicUtils as cryptoUtils

class Issuer(models.Model):
    id= UuidField( primary_key= True )
    crypt_description = models.CharField(max_length=96)
    
    def _set_description(self, value):
        self.crypt_description= cryptoUtils.encrypt_attrib( value )
        
    def _get_description(self):
        return cryptoUtils.decrypt_attrib( self.crypt_description )
    
    description= property( _get_description, _set_description )
    
    def __unicode__(self):
        return u"%s" % self.description

class IssuerAdmin(admin.ModelAdmin):
    pass

admin.site.register(Issuer, IssuerAdmin)

class TypeDocument(models.Model):
    crypt_description = models.CharField(max_length=96)
    mask = models.CharField(max_length=30, blank=True)
    
    def _set_description(self, value):
        self.crypt_description= cryptoUtils.encrypt_attrib( value )
        
    def _get_description(self):
        return cryptoUtils.decrypt_attrib( self.crypt_description )
    
    description= property( _get_description, _set_description )
    
    def __unicode__(self):
        return u"%s" % self.description

class TypeDocumentAdmin(admin.ModelAdmin):
    pass

admin.site.register(TypeDocument, TypeDocumentAdmin)


class Document(models.Model):
    id= UuidField( primary_key= True )
    typeDocument = models.ForeignKey(TypeDocument)
    crypt_document = models.CharField(max_length=96)
    issuer = models.ForeignKey(Issuer, null=True, blank=True)
    state = models.ForeignKey(State, null=True, blank=True)
    
    #Generic Relationship
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
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