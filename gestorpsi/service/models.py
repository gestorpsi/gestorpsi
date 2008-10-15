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
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from gestorpsi.organization.models import Organization, AgeGroup, Procedure
from gestorpsi.careprofessional.models import CareProfessional, Profession
from gestorpsi.util.uuid_field import UuidField
from gestorpsi.organization.models import Agreement

class Area(models.Model):
    title = models.CharField(max_length = 100)
    modality = models.ManyToManyField('Modality', null=True, blank=True)
    # Generic Relationship
    content_type = models.ForeignKey(ContentType)
    object_id = models.CharField(max_length=36)
    content_object = generic.GenericForeignKey()
    
    def __unicode__(self):
        return u'%s' % self.title

class ServiceType(models.Model):
    """
    This class holds information on available service types.
    @author: Vinicius H. S. Durelli
    @version: 1.0
    """
    name= models.CharField( max_length= 80 )
    description= models.CharField( max_length= 100, blank=True )
    area = models.ForeignKey(Area)

    def __unicode__(self):
        return u'%s' % self.name

class Modality(models.Model):
    """
    Instances of this class are created to represent modalities. Modalities have a name and a description.
    @author: Vinicius H. S. Durelli
    @version: 1.0
    """
    name= models.CharField( max_length= 80 )
    
    def __unicode__(self):
        return u'%s' % self.name


class AreaArt(models.Model):
    area = generic.GenericRelation(Area, null=True)

    def __unicode__(self):
        return u'%s' % self.area.content_type

class AreaBioPsychology(models.Model):
    area = generic.GenericRelation(Area, null=True)

    def __unicode__(self):
        return u'%s' % self.area.content_type

class AreaClinic(models.Model):
    age_group = models.ManyToManyField(AgeGroup, null=True)
    area = generic.GenericRelation(Area, null=True)
    service = generic.GenericRelation('Service', null=True)

    def __unicode__(self):
        return u'%s' % self.area.content_type

class AreaComparative(models.Model):
    area = generic.GenericRelation(Area, null=True)

    def __unicode__(self):
        return u'%s' % self.area.content_type

class AreaCommunity(models.Model):
    area = generic.GenericRelation(Area, null=True)

    def __unicode__(self):
        return u'%s' % self.area.content_type

class AreaEducational(models.Model):
    area = generic.GenericRelation(Area, null=True)

    def __unicode__(self):
        return u'%s' % self.area.content_type

class AreaSchool(models.Model):
    education_modality= models.CharField( max_length= 80 )
    area = generic.GenericRelation(Area, null=True)

    def __unicode__(self):
        return u'%s' % self.area.content_type

class AreaSport(models.Model):
    area = generic.GenericRelation(Area, null=True)

    def __unicode__(self):
        return u'%s' % self.area.content_type

class AreaExperimental(models.Model):
    area = generic.GenericRelation(Area, null=True)

    def __unicode__(self):
        return u'%s' % self.area.content_type

class AreaForensic(models.Model):
    area = generic.GenericRelation(Area, null=True)

    def __unicode__(self):
        return u'%s' % self.area.content_type

class AreaLegal(models.Model):
    area = generic.GenericRelation(Area, null=True)

    def __unicode__(self):
        return u'%s' % self.area.content_type

class AreaHospital(models.Model):
    area = generic.GenericRelation(Area, null=True)

    def __unicode__(self):
        return u'%s' % self.area.content_type

class AreaNeuropsychology(models.Model):
    area = generic.GenericRelation(Area, null=True)

    def __unicode__(self):
        return u'%s' % self.area.content_type

class AreaOrganizational(models.Model):
    hierarchical_level= models.CharField( max_length= 80 )
    area = generic.GenericRelation(Area, null=True)

    def __unicode__(self):
        return u'%s' % self.area.content_type

class AreaPsychoPedagogy(models.Model):
    area = generic.GenericRelation(Area, null=True)

    def __unicode__(self):
        return u'%s' % self.area.content_type

class AreaSocialPsychology(models.Model):
    area = generic.GenericRelation(Area, null=True)

    def __unicode__(self):
        return u'%s' % self.area.content_type

class AreaPsychomotricity(models.Model):
    area = generic.GenericRelation(Area, null=True)

    def __unicode__(self):
        return u'%s' % self.area.content_type

class AreaHealth(models.Model):
    area = generic.GenericRelation(Area, null=True)

    def __unicode__(self):
        return u'%s' % self.area.content_type

class AreaTransit(models.Model):
    area = generic.GenericRelation(Area, null=True)

    def __unicode__(self):
        return u'%s' % self.area.content_type

    
class ResearchProject(models.Model):
    """
    This class holds information related to research projects.
    @author: Vinicius H. S. Durelli
    @version: 1.0
    """
    name= models.CharField( max_length= 45 )
    description= models.CharField( max_length= 80 )
    
    def __unicode__(self):
        return u'%s' % self.name

class Service(models.Model):
    """
    This class is used to maintain information on services.
    @author: Vinicius H. S. Durelli
    @version: 1.0
    """
    id = UuidField(primary_key=True)
    name = models.CharField(max_length=80)
    description = models.CharField(max_length=100)
    keywords = models.CharField(max_length=100)
    active= models.BooleanField(default=True)
    area = models.ForeignKey(Area)
    service_type = models.ForeignKey(ServiceType)
    modalities = models.ManyToManyField(Modality)
    procedures = models.ManyToManyField(Procedure)
    agreements= models.ManyToManyField(Agreement)
    professions = models.ManyToManyField(Profession)

    # Generic Clinic Area Relationship
    content_type = models.ForeignKey(ContentType, null=True)
    object_id = models.CharField(max_length=36)
    content_object = generic.GenericForeignKey()
    
    research_project = models.ForeignKey( ResearchProject, null=True )    
    organization = models.ForeignKey(Organization, null=True)
    organization = models.ForeignKey(Organization, null=True)
    responsibles = models.ManyToManyField( CareProfessional )
    professionals = models.ManyToManyField( CareProfessional )

    def __unicode__(self):
        return u"%s" % (self.name)
    
    class Meta:
        ordering = ['name']