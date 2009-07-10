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
from gestorpsi.careprofessional.models import CareProfessional

class Approaches(models.Model):
    """
    Represents the necessary approaches (theoric reference) for psychologist
    @author: Danilo S. Sanches
    @version: 1.0  
    """    
    description = models.CharField(max_length=50)
    def __unicode__(self):
        return u"%s" % self.description
    class Meta:
        ordering = ['description']

class Area(models.Model):
    """
    Represents psychologist's specialist area
    @author: Danilo S. Sanches
    @version: 1.0 
    """
    description = models.CharField(max_length=30)
    def __unicode__(self):
        return u"%s" % self.description
    class Meta:
        ordering = ['description']

class AgeGroup(models.Model):
    """
    This class represents the AgeGroup that psychologist works
    @author: Danilo S. Sanches
    @version: 1.0  
    """
    description = models.CharField(max_length=30)
    def __unicode__(self):
        return u"%s" % self.description
    class Meta:
        ordering = ['description']

class Psychologist(CareProfessional):
     """
     This class represents a psychologist model. This  model needs some fields from CareProfessional and for this, an inherit from CareProfessional was used.        
     @author: Danilo S. Sanches
     @version: 1.0
     @see: CareProfessional
     """
     approaches = models.OneToOneField(Approaches, null=True)
     specialistArea = models.ForeignKey(Area, null=True)
     ageGroup = models.OneToOneField(AgeGroup, null=True)
