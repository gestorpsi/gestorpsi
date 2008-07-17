from django.db import models
from django.contrib.contenttypes import generic
from gestorpsi.phone.models import Phone
from gestorpsi.address.models import Country, City, Address
from gestorpsi.document.models import Document

# to be deleted
GENDER_CHOICES = (
    ('M','MALE'),
    ('F','FEMALE'),
)

# to be deleted
MARITAL_CHOICES = (
    ('0','SINGLE'),
    ('1','MARRIED'),
    ('2','DIVORCED'),
    ('3','COHABITATING'),
    ('4','NO_INFORMATION'),
)

class Gender(models.Model):
    description = models.CharField(max_length=15)
    def __unicode__(self):
        return self.description

class MaritalStatus(models.Model):
    description = models.CharField(max_length=20)
    def __unicode__(self):
        return self.description

class Person(models.Model):
    firstName = models.CharField('First Name', max_length=30)
    lastName = models.CharField('Last Name', max_length=30)
    nickname = models.CharField('Nickname', max_length=20, null=True)
    photo = models.ImageField('Photo', upload_to="client_photos", null=True)
    birthDate = models.DateField('Birthdate', null=True)
    birthPlace = models.ForeignKey(City, null=True)
    #gender = models.CharField('Gender',max_length=1, choices=GENDER_CHOICES)
    #maritalStatus = models.CharField('', max_length=1, choices=MARITAL_CHOICES)
    gender = models.ForeignKey(Gender)
    maritalStatus = models.ForeignKey(MaritalStatus)
    nationality = models.ForeignKey(Country)
    active = models.BooleanField(default=True)
    
    phones = generic.GenericRelation(Phone, null=True)
    address = generic.GenericRelation(Address, null=True)
    document = generic.GenericRelation(Document, null=True)
    
    def __unicode__(self):
        return self.name
    class Meta:
        ordering = ['firstName']