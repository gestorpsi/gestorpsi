# -*- coding: utf-8 -*-
from django.db import models
from django.forms import ModelForm
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib import admin
from gestorpsi.util import audittrail
from gestorpsi.util.uuid_field import UuidField
from gestorpsi.util import CryptographicUtils as cryptoUtils

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
    name = models.CharField(max_length=50)
    state = models.ForeignKey(State)
    def __unicode__(self):
        return u"%s (%s)" % (self.name, self.state.shortName)
    class Meta:
        ordering = ['name']

class AddressType(models.Model):
    description = models.CharField(max_length=20)
    def __unicode__(self):
        return u"%s" % self.description

class AddressTypeAdmin(admin.ModelAdmin):
    pass

admin.site.register(AddressType, AddressTypeAdmin)    

class Address(models.Model):
    # Brazil Address
    id= UuidField( primary_key= True )
    addressPrefix = models.CharField(max_length=10)
    crypt_addressLine1 = models.CharField(max_length=312, blank=True)
    crypt_addressLine2 = models.CharField(max_length=312, blank=True)
    crypt_addressNumber = models.CharField(max_length=56, blank=True)
    neighborhood = models.CharField(max_length=30, blank=True)
    crypt_zipCode = models.CharField(max_length=56, blank=True)
    addressType = models.ForeignKey(AddressType)
    city = models.ForeignKey(City, null=True)
    # Foreign Address
    foreignCountry = models.ForeignKey(Country, null=True)
    foreignState   = models.CharField(max_length=20, blank=True)
    foreignCity    = models.CharField(max_length=50, blank=True)
    # Generic Relationship
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()
    
    def _set_addressLine1(self, value):
        self.crypt_addressLine1= cryptoUtils.encrypt_attrib( value )
        
    def _get_addressLine1(self):
        return cryptoUtils.decrypt_attrib( self.crypt_addressLine1 )
    
    def _set_addressLine2(self, value):
        self.crypt_addressLine2= cryptoUtils.encrypt_attrib( value )
        
    def _get_addressLine2(self):
        return cryptoUtils.decrypt_attrib( self.crypt_addressLine2 )
    
    def _set_addressNumber(self, value):
        self.crypt_addressNumber= cryptoUtils.encrypt_attrib( value )
        
    def _get_addressNumber(self):
        return cryptoUtils.decrypt_attrib( self.crypt_addressNumber )
    
    def _set_zipCode(self, value):
        self.crypt_zipCode= cryptoUtils.encrypt_attrib( value )
        
    def _get_zipCode(self):
        return cryptoUtils.decrypt_attrib( self.crypt_zipCode )

    addressLine1= property( _get_addressLine1, _set_addressLine1 )
    addressLine2= property( _get_addressLine2, _set_addressLine2 )
    addressNumber= property( _get_addressNumber, _set_addressNumber )
    zipCode= property( _get_zipCode, _set_zipCode )
    
    history= audittrail.AuditTrail()
        
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
    
class AddressForm(ModelForm):
    class Meta:
        model= Address