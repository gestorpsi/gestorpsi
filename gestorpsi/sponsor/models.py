# -*- coding: utf-8 -*-
from django.db import models
from django.forms import ModelForm
from django.contrib.contenttypes import generic
from gestorpsi.phone.models import Phone
from gestorpsi.person.models import Person
from gestorpsi.internet.models import Email, Site, InstantMessenger
from gestorpsi.address.models import Country, City, Address
from gestorpsi.organization.models import Organization

class TaxWithHold(models.Model):
    """    
    This class represents a TaxWithHold type      
    @author: Danilo S. Sanches
    @version: 1.0 
    """
    description = models.CharField(max_length=50)
    def __unicode__(self):
        """
        returns a representation of this TaxWithHold as an unicode  C{string}.
        """
        return u"%s" % self.description

class Sponsor(models.Model):
    """    
    This class represents a sponsor of organizations. 
    This sponsor doesn't need to exist before of organization.       
    @author: Danilo S. Sanches
    @version: 1.0 
    """
    name = models.CharField(max_length=100)    
    companyID = models.CharField(max_length=100, null=True)
    healthRegion = models.CharField(max_length=10, null=True)
    bankBranch = models.CharField(max_length=10, null=True)
    account = models.CharField(max_length=15, null=True)
    
    taxWithHold = models.OneToOneField(TaxWithHold, null=True)
        
    phones = generic.GenericRelation(Phone, null=True)
    address = generic.GenericRelation(Address, null=True) 
    emails  = generic.GenericRelation(Email, null=True)
    sites = generic.GenericRelation(Site, null=True)
    instantMessengers =generic.GenericRelation(InstantMessenger, null=True)       
    
    organization = models.ForeignKey(Organization, null=True)
                          
    def __unicode__(self):
        """
        returns a representation of this sponsor as an unicode  C{string}.
        """
        return self.name