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

import reversion
from django.db import models
from gestorpsi.person.models import Person
from gestorpsi.place.models import Place
from gestorpsi.util.uuid_field import UuidField
from gestorpsi.organization.models import Agreement
from gestorpsi.phone.models import Phone
from gestorpsi.address.models import Address
from gestorpsi.internet.models import Email, Site, InstantMessenger

class InstitutionType(models.Model):
    """    
    This class represents an institution type.   
    @author: Danilo S. Sanches
    @version: 1.0 
    """
    description = models.CharField(max_length=50, null=True)
    def __unicode__(self):
        return u"%s" % self.description

reversion.register(InstitutionType)

class PostGraduate(models.Model):
    """    
    An instance of this class represents the postgraduate of careprofessional. This instance is relation on with careprofessional's academic resume      
    @author: Danilo S. Sanches
    @version: 1.0 
    """
    description = models.CharField(max_length=50, null=True)
    def __unicode__(self):
        return u"%s" % self.description

class AcademicResume(models.Model):
    """    
    This class represents careprofessional's academic resume       
    @author: Danilo S. Sanches
    @version: 1.0 
    """
    id= UuidField( primary_key= True )
    teachingInstitute = models.CharField(max_length=100, null=True)
    institutionType = models.OneToOneField(InstitutionType, null=True)
    course = models.CharField(max_length=100, null=True)
    initialDateGraduation = models.DateField(null=True)
    finalDateGraduation = models.DateField(null=True)
    lattesResume = models.URLField(null=True)
    postGraduate = models.ForeignKey(PostGraduate, null=True)
    initialDatePostGraduate = models.DateField(null=True)
    finalDatePostGraduate = models.DateField(null=True)
    area = models.CharField(max_length=100, null=True)    

    def revision(self):
        return reversion.models.Version.objects.get_for_object(self).order_by('-revision__date_created').latest('revision__date_created').revision

reversion.register(AcademicResume, follow='institutionType')

class Profession(models.Model):
    """    
    This class represents the careprofessional's profession       
    @author: Danilo S. Sanches
    @version: 1.0 
    """
    number = models.CharField(max_length=20, null=True)
    description = models.CharField(max_length=50, null=True)
    def __unicode__(self):
        return u"%s" % self.description

reversion.register(Profession)

class ProfessionalProfile(models.Model):
    """
    This class represents the professional profile
    @author: Danilo S. Sanches
    @version: 1.0
    """
    id= UuidField( primary_key= True )
    academicResume = models.OneToOneField(AcademicResume, null=True)
    initialProfessionalActivities = models.DateField(null=True)
    agreement = models.ManyToManyField(Agreement, null=True)
    profession = models.OneToOneField(Profession, null=True)
    services = models.CharField(max_length=100, null=True)
    availableTime = models.CharField(max_length=100, null=True)
    workplace = models.ManyToManyField(Place, null=True)
    
    def __unicode__(self):
        return '%s' % ( self.initialProfessionalActivities )

    def revision(self):
        return reversion.models.Version.objects.get_for_object(self).order_by('-revision__date_created').latest('revision__date_created').revision

reversion.register(ProfessionalProfile, follow=['academicResume', 'agreement', 'profession', 'workplace'])

class LicenceBoard(models.Model):
    """
    This class represents the careprofessional's licence board
    @author: Danilo S. Sanches
    @version: 1.0
    """
    name = models.CharField(max_length=20, null=True)
    description = models.CharField(max_length=100, null=True)
    
    def __unicode__(self):
        return self.name

class ProfessionalIdentification(models.Model):
    """
    This class represents the professional identification that is composed by careprofessional's licence board and register number 
    @author: Danilo S. Sanches
    @version: 1.0
    """
    id= UuidField( primary_key= True )
    licenceBoard = models.ForeignKey(LicenceBoard, null=True)
    registerNumber = models.CharField(max_length=50, null=True)    
    
    def __unicode__(self):
        return self.registerNumber

reversion.register(ProfessionalIdentification)

class CareProfessional(models.Model):
    """
    This class represents a careprofessional 
    @author: Danilo S. Sanches
    @version: 1.0
    """
    id= UuidField( primary_key= True )
    professionalIdentification = models.OneToOneField(ProfessionalIdentification, null=True)
    professionalProfile = models.OneToOneField(ProfessionalProfile, null = True)
    person = models.OneToOneField(Person)
    comments = models.CharField(max_length=200, null=True)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return u"%s" % self.person

    def revision(self):
        return reversion.models.Version.objects.get_for_object(self).order_by('-revision__date_created').latest('revision__date_created').revision

reversion.register(CareProfessional, follow=['person', 'professionalIdentification', 'professionalProfile'])


