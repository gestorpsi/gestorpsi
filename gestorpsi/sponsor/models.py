from django.db import models
from django.forms import ModelForm
from django.contrib.contenttypes import generic
from gestorpsi.phone.models import Phone
from gestorpsi.person.models import Person
from gestorpsi.internet.models import Email, Site, InstantMessenger
from gestorpsi.address.models import Country, City, Address
from gestorpsi.organization.models import Organization
from django.contrib import admin

class TaxWithHold(models.Model):
    description = models.CharField(max_length=50)
    def __unicode__(self):
        return u"%s" % self.description

class TaxWithHoldAdmin(admin.ModelAdmin):
    pass

admin.site.register(TaxWithHold, TaxWithHoldAdmin)


class Sponsor(models.Model):
    name = models.CharField('name',max_length=100)    
    companyID = models.CharField('companyID',max_length=100, null=True)
    healthRegion = models.CharField('healthRegion',max_length=10, null=True)
    bankBranch = models.CharField('bankBranch',max_length=10, null=True)
    account = models.CharField('account',max_length=15, null=True)
    
    taxWithHold = models.OneToOneField(TaxWithHold, null=True)
        
    phones = generic.GenericRelation(Phone, null=True)
    address = generic.GenericRelation(Address, null=True) 
    emails  = generic.GenericRelation(Email, null=True)
    sites = generic.GenericRelation(Site, null=True)
    instantMessengers =generic.GenericRelation(InstantMessenger, null=True)       
    
    organization = models.ForeignKey(Organization, null=True)
                          
    def __unicode__(self):
        return self.name    

class SponsorAdmin(admin.ModelAdmin):
    pass

admin.site.register(Sponsor, SponsorAdmin)