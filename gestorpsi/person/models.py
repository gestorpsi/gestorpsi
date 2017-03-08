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
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from gestorpsi.middleware import threadlocals
from gestorpsi.phone.models import Phone
from gestorpsi.address.models import City, Address, Country
from gestorpsi.document.models import Document
from gestorpsi.internet.models import Email, Site, InstantMessenger
from gestorpsi.organization.models import Organization
from gestorpsi.util.uuid_field import UuidField
from gestorpsi.util.first_capitalized import first_capitalized
from gestorpsi.util.models import Cnae
from datetime import datetime

Gender = (
    ('0','No Information'),
    ('1','Female'),
    ('2','Male')
)

COMPANY_SIZE = (
    (1, _('Small')),
    (2, _('Medium')),
    (3, _('Big')),
)


class MaritalStatus(models.Model):
    description = models.CharField(max_length=20)
    def __unicode__(self):
        return u"%s" % self.description
    class Meta:
        ordering = ['description']


class Person(models.Model):
    id = UuidField(primary_key=True)
    user = models.ForeignKey(User, editable=False, default=threadlocals.get_current_user) # the register owner
    name = models.CharField(max_length=50)
    nickname = models.CharField(max_length=50, null=True, blank=True)
    photo = models.ImageField(upload_to='Imagens', verbose_name=_("Imagens"))
    birthDate = models.DateField(null=True)
    birthPlace = models.ForeignKey(City, null=True)
    birthDateSupposed = models.BooleanField(default=False)
    gender = models.CharField(max_length=1, choices=Gender) 
    maritalStatus = models.ForeignKey(MaritalStatus, null=True)
    phones = generic.GenericRelation(Phone, null=True)
    address = generic.GenericRelation(Address, null=True)
    document = generic.GenericRelation(Document, null=True)
    emails  = generic.GenericRelation(Email, null=True)
    sites = generic.GenericRelation(Site, null=True)
    instantMessengers =generic.GenericRelation(InstantMessenger, null=True)
    comments = models.TextField(blank=True)
    active = models.BooleanField(default=True)
    organization = models.ManyToManyField(Organization)
    salary = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)

    # the fields below were added in order to deal with foreign ones
    birthForeignCity = models.CharField(max_length=100, null=True)
    birthForeignState = models.CharField(max_length=100, null=True)
    birthForeignCountry = models.IntegerField(max_length=4, null=True)
        
    def __unicode__(self):
        return (u"%s (%s)" % (self.name.title(), _('Company'))) if self.is_company() else (u"%s" % (self.name.title()))

    def save(self, *args, **kwargs):
        super(Person, self).save(*args, **kwargs)
        if not self.id:
            for p in self.organization_set.all():
                p.employee_number = p.care_professionals()
                p.save()
    
    def delete(self, *args, **kwargs):
        super(Person, self).delete(*args, **kwargs)
        for p in self.organization_set.all():
            p.employee_number = p.care_professionals()
            p.save()


    """ function used only in reports.py waiting a fix in Geraldo SubReport"""
    def get_documents(self):
        if self.document.all().count() > 1:
            text = u"%s " % self.document.all()[0]
            text += u" | %s" % self.document.all()[1]
        elif self.document.all().count() == 1:
            text = u"%s" % self.document.all()[0]
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
        #TODO: NEED FIX THIS BUG WHEN GENERATING CLIENT PDF WITH PHOTO
        #      PERSON HAS A M2M RELATIONSHIP TO ORGANIZATION, NOT ONE-TO-ONE
        #if len(self.photo):
        #    return "%simg/organization/%s/.thumb-whitebg/%s" % (MEDIA_ROOT, self.organization.id, self.photo)
        #else:
        #    return "%simg/%s" % (MEDIA_ROOT, 'male_generic_photo.png')
        return "%s/img/%s" % (MEDIA_ROOT, 'male_generic_photo.png')

    def get_birthdate(self):
        if self.birthDate == None:
            return ""
        else:
            return self.birthDate.strftime('%d/%m/%Y')

    def get_first_phone(self):
        if self.phones.all().count():
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

    def get_age(self):
        if not self.birthDate:
            return None

        today = datetime.today()
        return (today.year - self.birthDate.year) - int((today.month, today.day) < (self.birthDate.month, self.birthDate.day))

    age = property(get_age)

    def is_company(self):
        return True if hasattr(self, 'company') else False

    def is_administrator(self):
        if not hasattr(self, 'profile'): 
            return False
        else:
            return False if not 'administrator' in [i.name for i in self.profile.user.groups.all()] else True

    def is_secretary(self):
        if not hasattr(self, 'profile'): 
            return False
        else:
            return False if not 'secretary' in [i.name for i in self.profile.user.groups.all()] else True

    def is_client(self):
        return True if hasattr(self, 'client') else False

    def is_careprofessional(self):
        return True if hasattr(self, 'careprofessional') and not hasattr(self.careprofessional, 'studentprofile') else False

    def is_student(self):
        return True if hasattr(self, 'careprofessional') and hasattr(self.careprofessional, 'studentprofile') else False

    def is_employee(self):
        return True if hasattr(self, 'employee') else False

    def revision(self):
        return reversion.get_for_object(self).order_by('-revision__date_created').latest('revision__date_created').revision

    def revision_created(self):
        return reversion.get_for_object(self).order_by('revision__date_created').latest('revision__date_created').revision

    class Meta:
        ordering = ['name']

class CompanyClient(models.Model):
    from gestorpsi.client.models import Client
    client = models.ForeignKey(Client)
    company = models.ForeignKey('Company')
    responsible = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return u'%s' % (self.client)

    class Meta:
        ordering = ['-active', '-responsible', 'client']
        unique_together = (('client', 'company'),)

class Company(models.Model):
    from gestorpsi.client.models import Client
    person = models.OneToOneField(Person, blank=True, null=True)
    size = models.IntegerField(_('Company Size'), blank=True, null=True, choices=COMPANY_SIZE)
    cnae_class = models.CharField(_('CNAE Subclass Code'), blank=True, null=True, max_length=9)
    client = models.ManyToManyField(Client, blank=True, through='CompanyClient')

    def __unicode__(self):
        return u'%s' % self.person.name
    
    def _cnae_class_name(self):
        c = Cnae.objects.filter(id=self.cnae_class)
        if len(c):
            return c[0].cnae_class
        return None
    cnae_class_name = property(_cnae_class_name)

reversion.register(Company)
reversion.register(CompanyClient)
reversion.register(Person)
