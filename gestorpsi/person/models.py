# -*- coding: utf-8 -*-
from django.db import models
from django.forms import ModelForm
from django.contrib.contenttypes import generic
from gestorpsi.phone.models import Phone
from gestorpsi.address.models import Country, City, Address
from gestorpsi.document.models import Document
from gestorpsi.internet.models import Email, Site, InstantMessenger
from gestorpsi.organization.models import Organization
from gestorpsi.util.uuid_field import UuidField
from gestorpsi.util import audittrail
from gestorpsi.util import CryptographicUtils as cryptoUtils
   
Gender = ( ('0','No Information'),('1','Female'), ('2','Male'))    

class MaritalStatus(models.Model):
    description = models.CharField(max_length=20)
    def __unicode__(self):
        return u"%s" % self.description

class Person(models.Model):
    id= UuidField( primary_key= True )
    crypt_name = models.CharField(max_length= 256 )
    crypt_nickname = models.CharField(max_length=250, null=True, blank=True)

    photo = models.CharField(max_length=100)
    birthDate = models.DateField(null=True)
    birthPlace = models.ForeignKey(City, null=True)
    gender = models.CharField(max_length=1, choices=Gender) 
    maritalStatus = models.ForeignKey(MaritalStatus, null=True)
    phones = generic.GenericRelation(Phone, null=True)
    address = generic.GenericRelation(Address, null=True)
    document = generic.GenericRelation(Document, null=True)
    emails  = generic.GenericRelation(Email, null=True)
    sites = generic.GenericRelation(Site, null=True)
    instantMessengers =generic.GenericRelation(InstantMessenger, null=True)
        
    organization = models.ForeignKey(Organization, null=True)
    
    history= audittrail.AuditTrail()
    
    def _get_name(self):
        return cryptoUtils.decrypt_attrib( self.crypt_name )
    
    def _set_name(self, value):
        self.crypt_name= cryptoUtils.encrypt_attrib( value )
        
    def _get_nickname(self):
        return cryptoUtils.decrypt_attrib( self.crypt_nickname )
    
    def _set_nickname(self, value):
        self.crypt_nickname= cryptoUtils.encrypt_attrib( value )
    
    name= property( _get_name, _set_name )
    nickname= property( _get_nickname, _set_nickname )
    
    def __unicode__(self):
        return u"%s" % self.name
    
    def get_first_phone(self):
        if ( len( self.phones.all() ) != 0 ):
            return self.phones.all()[0]
        else:
            return ''
    
    def get_first_email(self):
        if ( len( self.emails.all() ) != 0 ):
            return self.emails.all()[0]
        else:
            return ''


class PersonForm(ModelForm):
    class Meta:
        model= Person
        
"""
Teste do Models no shell de Pessoa e suas ligacoes

from gestorpsi.person.models import Person, MaritalStatus, Gender
from gestorpsi.phone.models import PhoneType, Phone
from gestorpsi.address.models import Address, AddressType, City, Country, State
from gestorpsi.document.models import Document, Issuer
from gestorpsi.internet.models import Email, Site, InstantMessenger, IMNetwork

p = Person()
#p.firstName = "Fulano"
#p.lastName = "da Silva"
p.firstName = "Fulano da Silva"
p.nickname = "Fulaninho"
p.birthPlace = City.objects.get(pk=44085)
p.gender = Gender.objects.get(pk=1)
p.maritalStatus = MaritalStatus.objects.get(pk=1)
p.nationality = Country.objects.get(pk=33)
p.save()

p.phones.create(area='11',phoneNumber='33442211',ext='123',phoneType=PhoneType.objects.get(pk=1))
p.phones.create(area='11',phoneNumber='98761234',ext='',phoneType=PhoneType.objects.get(pk=2))

address = Address()
address.addressPrefix = "Rua"
address.addressLine1 = "Rui Barbosa, 1234"
address.addressLine2 = "Anexo II - Sala 4"
address.neighborhood = "Centro"
address.zipCode = "12345-123"
address.addressType = AddressType.objects.get(pk=1)
address.city = City.objects.get(pk=44085)
address.content_object = p
address.save()

p.document.create(identityCard='23.232.232-2',issuer=Issuer.objects.get(pk=1),state=State.objects.get(pk=24),cpf='434.343.343-34')

p.emails.create(email='bla@uol.com.br')
p.emails.create(email='ble@uol.com.br')
p.emails.create(email='bli@uol.com.br')
p.emails.create(email='blo@uol.com.br')
p.emails.create(email='blu@uol.com.br')

p.sites.create(description='Meu site',site='http://www.uol.com.br')
p.sites.create(description='Meu blog',site='http://bla.blog.uol.com.br')
p.sites.create(description='Meu orkut',site='http://www.orkut.com/747463636')

p.instantMessengers.create(identity='7373234',network=IMNetwork.objects.get(pk=1))
"""