from django.db import models
from django.newforms import ModelForm
from django.contrib.contenttypes import generic
from gestorpsi.sponsor.models import Sponsor
from gestorpsi.phone.models import Phone
from gestorpsi.person.models import Person
from gestorpsi.internet.models import Email, Site, InstantMessenger
from gestorpsi.address.models import Country, City, Address

class PersonType(models.Model):
    description = models.CharField(max_length=30)
    def __unicode__(self):
        return u"%s" % self.description
    class Admin: pass

class AdministrationType(models.Model):
    description = models.CharField(max_length=30)
    def __unicode__(self):
        return u"%s" % self.description
    class Admin: pass

class Dependency(models.Model):
    description = models.CharField(max_length=30)
    def __unicode__(self):
        return u"%s" % self.description
    class Admin: pass

class FacilityType(models.Model):
    description = models.CharField(max_length=100)
    def __unicode__(self):
        return u"%s" % self.description
    class Admin: pass

class CareType(models.Model):
    description = models.CharField(max_length=50)
    def __unicode__(self):
        return u"%s" % self.description
    class Admin: pass

class Management(models.Model):
    description = models.CharField(max_length=50)
    def __unicode__(self):
        return u"%s" % self.description
    class Admin: pass
    
class OrganizationType(models.Model):
    description = models.CharField(max_length=50)
    def __unicode__(self):
        return u"%s" % self.description
    class Admin: pass

class ResearchEducationActivities(models.Model):
    description = models.CharField(max_length=50)
    def __unicode__(self):
        return u"%s" % self.description
    class Admin: pass


class Organization(models.Model):
    #Identification
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
    
    active = models.BooleanField(default=True)
    icon = models.CharField('icon', max_length=30)          
    
    #Profile
    personType = models.OneToOneField(PersonType, null=True)
    administrationType = models.OneToOneField(AdministrationType, null=True)
    dependency = models.OneToOneField(Dependency, null=True)
    facilityType = models.OneToOneField(FacilityType, null=True)
    careType = models.OneToOneField(CareType, null=True)
    management = models.OneToOneField(Management, null=True)
    organizationType = models.OneToOneField(OrganizationType, null=True)
    researchEducationActivities = models.OneToOneField(ResearchEducationActivities, null=True)
    
    phones = generic.GenericRelation(Phone, null=True)
    address = generic.GenericRelation(Address, null=True)
    emails  = generic.GenericRelation(Email, null=True)
    sites = generic.GenericRelation(Site, null=True)
    instantMessengers =generic.GenericRelation(InstantMessenger, null=True)
    organization = models.ForeignKey('self', related_name="%(class)s_related", null=True)
    
    sponsor = models.ForeignKey(Sponsor, null=True)    
    
                          
    def __unicode__(self):
        return self.name    
    
    class Admin:
        pass