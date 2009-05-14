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
from django.contrib.contenttypes import generic
from gestorpsi.phone.models import Phone
from gestorpsi.address.models import City, Address, Country
from gestorpsi.document.models import Document
from gestorpsi.internet.models import Email, Site, InstantMessenger
from gestorpsi.organization.models import Organization
from gestorpsi.util.uuid_field import UuidField
from gestorpsi.util.first_capitalized import first_capitalized
   
Gender = ( ('0','No Information'),('1','Female'), ('2','Male'))

class MaritalStatus(models.Model):
    description = models.CharField(max_length=20)
    def __unicode__(self):
        return u"%s" % self.description

class Person(models.Model):
    id = UuidField(primary_key=True)
    name = models.CharField(max_length=50)
    nickname = models.CharField(max_length=20, null=True, blank=True)

    photo = models.CharField(max_length=100)
    birthDate = models.DateField(null=True)
    birthPlace = models.ForeignKey(City, null=True)
    
    #the fields below were added in order to deal with foreign ones
    birthForeignCity = models.CharField(max_length=100, null=True)
    birthForeignState = models.CharField(max_length=100, null=True)
    birthForeignCountry = models.IntegerField(max_length=4, null=True)
    ###############################################################
    
    gender = models.CharField(max_length=1, choices=Gender) 
    maritalStatus = models.ForeignKey(MaritalStatus, null=True)
    phones = generic.GenericRelation(Phone, null=True)
    address = generic.GenericRelation(Address, null=True)
    document = generic.GenericRelation(Document, null=True)
    emails  = generic.GenericRelation(Email, null=True)
    sites = generic.GenericRelation(Site, null=True)
    instantMessengers =generic.GenericRelation(InstantMessenger, null=True)
        
    organization = models.ForeignKey(Organization, null=True)

    """ function used only in reports.py waiting a fix in Geraldo SubReport"""
    def get_documents(self):
        if self.document.all().count() > 1:
            text = "%s " % self.document.all()[0]
            text += " | %s" % self.document.all()[1]
        elif self.document.all().count() == 1:
            text = "%s" % self.document.all()[0]
        else:
            text = ""
        return text

    """ function used only in reports.py waiting a fix in Geraldo SubReport"""
    def get_phones(self):
        if self.phones.all().count() > 1:
            text = "%s " % self.phones.all()[0]
            text += " | %s" % self.phones.all()[1]
        elif self.phones.all().count() == 1:
            text = "%s" % self.phones.all()[0]
        else:
            text = ""
        return text

    """ function used only in reports.py waiting a fix in Geraldo SubReport"""
    def get_internet(self):
        text = ""
        if self.emails.all().count():
            text = "e-mail: %s" % self.emails.all()[0]
        if self.sites.all().count():
            if len(text):
                text += " | Web Page: %s" % self.sites.all()[0]
            else:
                text += "Web Page: %s" % self.sites.all()[0]
        if self.instantMessengers.all().count():
            if len(text):
                text += " | IM: %s" % self.instantMessengers.all()[0]
            else:
                text += "IM: %s" % self.instantMessengers.all()[0]
        return text

    """ function used only in reports.py waiting a fix in Geraldo SubReport"""
    def get_address(self):
        text = ""
        if self.address.all().count():
            addr = self.address.all()[0]
            text = "%s %s, %s" % (addr.addressPrefix, addr.addressLine1, addr.addressNumber)
            if len(addr.addressLine2): text += " - %s" % addr.addressLine2
            if len(addr.neighborhood): text += " - %s" % addr.neighborhood
            text += "<br />%s - %s - %s" % (first_capitalized(addr.city.name), addr.city.state.shortName, addr.city.state.country.name)
            if len(addr.zipCode): text += " - CEP: %s" % addr.zipCode
        return text

    def get_photo(self):
        from gestorpsi.settings import MEDIA_ROOT #, PROJECT_ROOT_PATH
        if len(self.photo):
            return "%simg/organization/%s/.thumb-whitebg/%s" % (MEDIA_ROOT, self.organization.id, self.photo)
        else:
            return "%simg/%s" % (MEDIA_ROOT, 'male_generic_photo.png')

    def get_birthdate(self):
        if self.birthDate == None:
            return ""
        else:
            return self.birthDate.strftime('%d/%m/%Y')

    def get_first_phone(self):
        if self.phones.count:
            return self.phones.all()[0]
        else:
            return ""

    def get_birth_place(self):
        if self.birthPlace == None:
            return u"%s - %s" % (self.birthForeignCity, self.birthForeignState)
        else:
            return u"%s - %s" % (first_capitalized(self.birthPlace.name), self.birthPlace.state.shortName)

    def get_birth_country(self):
        if self.birthPlace == None:
            return u"%s" % Country.objects.get(pk=self.birthForeignCountry)
        else:
            return self.birthPlace.state.country

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
        
    def get_first_site(self):
        if ( len( self.sites.all() ) != 0 ):
            return self.sites.all()[0]
        else:
            return ''        

reversion.register(Person, follow=['phones','address', 'emails', 'sites', 'instantMessengers'])


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
