from django.db import models
from django.contrib.contenttypes import generic
from gestorpsi.phone.models import Phone
from gestorpsi.address.models import Country, City, Address
from gestorpsi.document.models import Document
from gestorpsi.internet.models import Email, Site, InstantMessenger

class Gender(models.Model):
    description = models.CharField(max_length=15)
    def __unicode__(self):
        return self.description
    class Admin: pass

class MaritalStatus(models.Model):
    description = models.CharField(max_length=20)
    def __unicode__(self):
        return self.description
    class Admin: pass

class Person(models.Model):
    firstName = models.CharField('First Name', max_length=30)
    lastName = models.CharField('Last Name', max_length=30)
    nickname = models.CharField('Nickname', max_length=20, null=True)
    photo = models.ImageField('Photo', upload_to="client_photos", null=True)
    birthDate = models.DateField('Birthdate', null=True)
    birthPlace = models.ForeignKey(City, null=True)
    gender = models.ForeignKey(Gender,null=True)
    maritalStatus = models.ForeignKey(MaritalStatus,null=True)
    # Reduntante pois ja temos birthPlace
    nationality = models.ForeignKey(Country)
    active = models.BooleanField(default=True)
    
    phones = generic.GenericRelation(Phone, null=True)
    address = generic.GenericRelation(Address, null=True)
    document = generic.GenericRelation(Document, null=True)
    emails  = generic.GenericRelation(Email, null=True)
    sites = generic.GenericRelation(Site, null=True)
    instantMessengers =generic.GenericRelation(InstantMessenger, null=True)
    def __unicode__(self):
        return self.firstName
    class Meta:
        ordering = ['firstName']