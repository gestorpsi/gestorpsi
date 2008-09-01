# -*- coding: utf-8 -*-
from django.db import models
from django.forms import ModelForm
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib import admin
from gestorpsi.util import audittrail
from gestorpsi.util.uuid_field import UuidField
from gestorpsi.util import CryptographicUtils as cryptoUtils

class EmailType(models.Model):
    description= models.CharField( max_length= 45 )
    def __unicode__(self):
        return self.description

class EmailTypeAdmin(admin.ModelAdmin):
    pass

admin.site.register(EmailType, EmailTypeAdmin)

class Email(models.Model):
    id= UuidField( primary_key= True )
    crypt_email = models.CharField( max_length= 232, blank=True)
    email_type = models.ForeignKey( EmailType )
    # Generic Relation
    content_type= models.ForeignKey(ContentType)
    object_id= models.PositiveIntegerField()
    content_object= generic.GenericForeignKey()
    
    def _set_email(self, value):
        self.crypt_email= cryptoUtils.encrypt_attrib( value )
        
    def _get_email(self):
        return cryptoUtils.decrypt_attrib( self.crypt_email )
    
    email= property( _get_email, _set_email )

    history = audittrail.AuditTrail()

    def __cmp__(self, other):
        if (self.email == other.email) and \
           (self.email_type == other.email_type):
            return 0
        else:
            return 1

    def __unicode__(self):
        return self.email

class EmailForm(ModelForm):
    class Meta:
        model= Email

class Site(models.Model):
    id= UuidField( primary_key= True )
    crypt_description = models.CharField(max_length=232, blank=True)
    crypt_site = models.CharField(max_length=232, blank=True)
    # Generic Relation
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()
    
    def _set_description(self, value):
        self.crypt_description= cryptoUtils.encrypt_attrib( value )
        
    def _get_description(self):
        return cryptoUtils.decrypt_attrib( self.crypt_description )
    
    def _set_site(self, value):
        self.crypt_site= cryptoUtils.encrypt_attrib( value )
        
    def _get_site(self):
        return cryptoUtils.decrypt_attrib( self.crypt_site )
    
    description= property( _get_description, _set_description )
    site= property( _get_site, _set_site )

    history = audittrail.AuditTrail()

    def __cmp__(self, other):
        if (self.description == other.description) and \
           (self.site == other.site):
            return 0
        else:
            return 1    
    
    def __unicode__(self):
        return self.site

class IMNetwork(models.Model):
    id= UuidField( primary_key= True )
    crypt_description = models.CharField(max_length=56)
    
    def _set_description(self, value):
        self.crypt_description= cryptoUtils.encrypt_attrib( value )
        
    def _get_description(self):
        return cryptoUtils.decrypt_attrib( self.crypt_description )
    
    description= property( _get_description, _set_description )

    def __unicode__(self):
        return self.description

class IMNetworkAdmin(admin.ModelAdmin):
    pass

admin.site.register(IMNetwork, IMNetworkAdmin)

class InstantMessenger(models.Model):
    id= UuidField( primary_key= True )
    crypt_identity = models.CharField(max_length=160, blank=True)
    network = models.ForeignKey(IMNetwork, blank=True)
    # Generic Relation
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()
    
    def _set_identity(self, value):
        self.crypt_identity= cryptoUtils.encrypt_attrib( value )
        
    def _get_identity(self):
        return cryptoUtils.decrypt_attrib( self.crypt_identity )
    
    identity= property( _get_identity, _set_identity )
    
    history = audittrail.AuditTrail()

    def __cmp__(self, other):
        if (self.identity == other.identity) and \
           (self.network == other.network):
            return 0
        else:
            return 1

    def __unicode__(self):
        return "%s (%s)" % (self.identity, self.network)