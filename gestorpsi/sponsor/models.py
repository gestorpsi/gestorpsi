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

from django.db import models
from django.contrib.contenttypes import generic
from gestorpsi.phone.models import Phone
from gestorpsi.internet.models import Email, Site, InstantMessenger
from gestorpsi.address.models import Address
from gestorpsi.organization.models import Organization
from gestorpsi.util.uuid_field import UuidField

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
    class Meta:
        ordering = ['description']

class Sponsor(models.Model):
    """    
    This class represents a sponsor of organizations. 
    This sponsor doesn't need to exist before of organization.       
    @author: Danilo S. Sanches
    @version: 1.0 
    """
    id= UuidField(primary_key=True)
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
    class Meta:
        ordering = ['name']

