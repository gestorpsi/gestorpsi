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
from django.forms import ModelForm
from django.contrib.contenttypes import generic
from gestorpsi.phone.models import Phone
from gestorpsi.internet.models import Email, Site, InstantMessenger
from gestorpsi.address.models import Country, City, Address
from gestorpsi.util.uuid_field import UuidField

class PersonType(models.Model):
    """
    This class represents a person type for organization profile. The person type can be (physical or juridical)  
    @author: Danilo S. Sanches
    @version: 1.0 
    """
    description = models.CharField(max_length=50)
    def __unicode__(self):
        return u"%s" % self.description

class UnitType(models.Model):
    """
    This class represents unity type  
    @author: Fabio Martins
    @version: 1.0 
    """
    description = models.CharField(max_length=255)
    def __unicode__(self):
        return u"%s" % self.description

class AdministrationEnvironment(models.Model):
    """
    This class represents a administration type of Organization. This administration type can be (municipal, state, federal or private)  
    @author: Fabio Martins
    @version: 1.0 
    """
    description = models.CharField(max_length=30)
    def __unicode__(self):
        return u"%s" % self.description

class Source(models.Model):
    """
    This class represents the organization situation
    @author: Fabio Martins
    @version: 1.0 
    """
    description = models.CharField(max_length=255)
    def __unicode__(self):
        return u"%s" % self.description

class ProvidedType(models.Model):
    """    
    This class represents a care type provided
    @author: Danilo S. Sanches
    @version: 1.0 
    """
    description = models.CharField(max_length=50)
    def __unicode__(self):
        return u"%s" % self.description

class Management(models.Model):
    """    
    This class represents a management type of organization 
    @author: Danilo S. Sanches
    @version: 1.0 
    """
    description = models.CharField(max_length=50)
    def __unicode__(self):
        return u"%s" % self.description

class Dependence(models.Model):
    """    
    This class represents a Dependence type
    @author: Fabio Martins
    @version: 1.0 
    """
    description = models.CharField(max_length=50)
    def __unicode__(self):
        return u"%s" % self.description

class Activitie(models.Model):
    """    
    This class represents the research activities from Organization.  
    @author: Danilo S. Sanches
    @version: 1.0 
    """
    description = models.CharField(max_length=255)
    def __unicode__(self):
        return u"%s" % self.description

class Organization(models.Model):
    """    
    This class represents the organization model.   
    @author: Danilo S. Sanches
    @version: 1.0 
    """
    id= UuidField(primary_key=True)
    
    # identity
    name = models.CharField(max_length=100)
    trade_name = models.CharField(max_length=100, blank=True)
    register_number = models.CharField(max_length=100, blank=True)
    cnes = models.CharField(max_length=100, blank=True)
    state_inscription = models.CharField(max_length=30, blank=True)
    city_inscription = models.CharField(max_length=30, blank=True)
    subscriptions_professional_institutional = models.CharField(max_length=100, blank=True)
    professional_responsible = models.CharField(max_length=100, blank=True) 
    
    # profile
    person_type = models.OneToOneField(PersonType, null=True, blank=True)
    unit_type = models.OneToOneField(UnitType, null=True, blank=True)
    environment = models.OneToOneField(AdministrationEnvironment, null=True, blank=True)
    management = models.OneToOneField(Management, null=True, blank=True)
    source = models.OneToOneField(Source, null=True, blank=True)
    dependence = models.OneToOneField(Dependence, null=True, blank=True)
    provided_type = models.ManyToManyField(ProvidedType, null=True, blank=True)
    activity = models.OneToOneField(Activitie, null=True, blank=True)
    
    comment = models.CharField(max_length=765, blank=True)
        
    active = models.BooleanField(default=True)
    
    photo = models.CharField(max_length=200, blank=True)          
    
    phones = generic.GenericRelation(Phone, null=True)
    address = generic.GenericRelation(Address, null=True)
    emails  = generic.GenericRelation(Email, null=True)
    sites = generic.GenericRelation(Site, null=True)
    instantMessengers =generic.GenericRelation(InstantMessenger, null=True) ### it needs more description    
    organization = models.ForeignKey('self', related_name="%(class)s_related", null=True, blank=True)
                              
    def __unicode__(self):
        return self.name

class AgreementType(models.Model):
    """
    This class represents an agreement type.
    @author: Vinicius H. S. Durelli
    @version: 1.0
    """
    description= models.CharField( max_length= 80 )
    def __unicode__(self):
        return u'%s' % self.description

class Agreement(models.Model):
    """
    This class represents an agreement type that the careprofessional works
    @author: Danilo S. Sanches
    @version: 1.0
    """
    description = models.CharField(max_length=50, null=True)
    def __unicode__(self):
        return u"%s" % self.description

class AgeGroup(models.Model):
    """
    This class was created to represent an interval of ages as follows: for instance,
    if some client is 6 years old and there is a instance of AgeGroup which represents and labels the
    interval between 0 and 8 as 'child', then such client will be classified as child since his/her age is contained
    in the bounded interval [0-8]*.
    *The interval [0-8] includes every number between 0 and 8 as well as 0 and 8.
    """
    minimum_age_endpoint= models.PositiveIntegerField()
    maximum_age_endpoint= models.PositiveIntegerField()
    label= models.CharField( max_length= 30, null= False )
    
    def __unicode__(self):
        return u"%s (%i-%i)" % ( self.label, self.minimum_age_endpoint, self.maximum_age_endpoint )
    class Meta:
        ordering = ['minimum_age_endpoint']    

class ProcedureProvider(models.Model):
    """
    This class was created to represent entities which provide some kind of health care service.
    """
    name= models.CharField( max_length= 20 )
    
    def __unicode__(self):
        return u"name: %s" % self.name

class Procedure(models.Model):
    """
    This class represents procedures provided by entities like the Sistema Único de Saúde (SUS).
    """
    procedure_code= models.CharField( max_length= 20, null= True )
    description= models.CharField( max_length= 255, null= False )
    procedure= models.ForeignKey( ProcedureProvider )

    def __unicode__(self):
        return u"code: %s, description: %s" % (self.procedure_code, self.description)