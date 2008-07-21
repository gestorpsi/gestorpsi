from django.db import models
from django.newforms import ModelForm
from django.contrib.contenttypes import generic
from gestorpsi.phone.models import Phone
from gestorpsi.person.models import Person
from gestorpsi.address.models import Country, City, Address



class Organization(models.Model):
    name = models.CharField('name',max_length=100)
    businessName = models.CharField('businessName',max_length=100, null=True)
    companyID = models.CharField('companyID',max_length=100, null=True)
    healthCompanyID = models.CharField('healthCompanyID',max_length=100, null=True)
    stateTaxID = models.CharField('stateTaxID',max_length=30, null=True)
    cityTaxID = models.CharField('cityTaxID',max_length=30, null=True)
    companyProfessionalLicense = models.CharField('companyProfessionalLicense',max_length=100, null=True)
    accountableProfessional = models.CharField('accountableProfessional',max_length=100, null=True) 
    email = models.EmailField('email', null=True)
    site = models.URLField('site', max_length=50, null=True)           
    
    phones = generic.GenericRelation(Phone, null=True)
    address = generic.GenericRelation(Address, null=True)
    organization = models.ForeignKey('self', related_name="%(class)s_related", null=True)    
    
                          
    def __unicode__(self):
        return self.name    
    
    class Admin:
        pass