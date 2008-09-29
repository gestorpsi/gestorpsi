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
from gestorpsi.organization.models import Organization
from gestorpsi.phone.models import Phone
from gestorpsi.address.models import Country, City, Address

# Create your models here.
#gender_list = (('M','Male'),('F','Female'))

#class Establishment(models.Model):
#    name = models.CharField('name',max_length=100)
#    email = models.EmailField('Email')
#    site = models.URLField('site', max_length=50)   
#    phones = generic.GenericRelation(Phone, null=True)
#    address = generic.GenericRelation(Address, null=True)           
     
#    def __unicode__(self):
#        return self.name    
    
#    class Admin:
#        pass
#class EstablishmentForm(ModelForm):
#    class Meta:
#        model= Establishment

#class CareProfessional(models.Model):
#    name = models.CharField('name',max_length=100, core=True)
#    gender = models.CharField(max_length=1, choices=gender_list)        
#    organization = models.ForeignKey(Organization, edit_inline = models.TABULAR, num_in_admin=1)
        
    
    
#    def __unicode__(self):
#        return self.name 
#    
#class CareProfessionalForm(ModelForm):
#    class Meta:
#        model= CareProfessional
       


    
    
   
