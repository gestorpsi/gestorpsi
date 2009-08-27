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
from django.utils.translation import ugettext as _
from gestorpsi.organization.models import Organization, Agreement, AgeGroup, EducationLevel, HierarchicalLevel, Procedure
from gestorpsi.careprofessional.models import CareProfessional, Profession
from gestorpsi.util.uuid_field import UuidField 

class ServiceType(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500, blank=True)

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        ordering = ['name']

class Modality(models.Model):
    name= models.CharField(max_length=100)
    
    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        ordering = ['name']

class Area(models.Model):
    area_name = models.CharField(_('Area Name'), max_length=100, blank=True, null=True)
    area_code = models.CharField(_('Area Code'), max_length=30, blank=True, null=True)
    service_type = models.ManyToManyField(ServiceType, null=True, blank=True)
    modalities = models.ManyToManyField(Modality, null=True, blank=True)
    age_group = models.ManyToManyField(AgeGroup, null=True, blank=True)
    education_level = models.ManyToManyField(EducationLevel, null=True, blank=True)
    hierarchical_level = models.ManyToManyField(HierarchicalLevel, null=True, blank=True)

    def __unicode__(self):
        return u"%s" % self.area_name

    class Meta:
        ordering = ['area_name']

class Service(models.Model):
    """
    This class is used to maintain information on services.
    @author: Gestorpsi
    @version: 1.0
    """
    id = UuidField(primary_key=True)
    name = models.CharField(max_length=80)
    description = models.CharField(max_length=999, blank=True)
    keywords = models.CharField(max_length=100, blank=True)
    active = models.BooleanField(default=True)
    area = models.ForeignKey(Area)
    service_type = models.ForeignKey(ServiceType)
    modalities = models.ManyToManyField(Modality)
    
    age_group = models.ManyToManyField(AgeGroup, null=True, blank=True)
    education_level = models.ManyToManyField(EducationLevel, null=True, blank=True)
    hierarchical_level = models.ManyToManyField(HierarchicalLevel, null=True, blank=True)
    
    agreements= models.ManyToManyField(Agreement)
    professions = models.ManyToManyField(Profession)
    research_project = models.BooleanField(default=False) 
    research_project_name = models.CharField(max_length=500)
    organization = models.ForeignKey(Organization, null=True)
    responsibles = models.ManyToManyField( CareProfessional, related_name="resp_services" )
    professionals = models.ManyToManyField( CareProfessional, related_name="prof_services" )
    css_color_class = models.IntegerField(max_length=2, blank=True, null=True, default=0)
    date = models.DateTimeField(auto_now_add=True)
    comments = models.TextField(blank=True)

    procedures = models.ManyToManyField(Procedure)

    def __unicode__(self):
        return u"%s" % (self.name)
    
    class Meta:
        ordering = ['name']
        get_latest_by = ['date']

    def groups(self):
        group = []
        for i in self.referral_set.all():
            if i.group_name():
                group.append(i.group_name())
        return group

    def revision(self):
        return reversion.models.Version.objects.get_for_object(self).order_by('-revision__date_created').latest('revision__date_created').revision

reversion.register(Service, follow=['modalities', 'agreements', 'professions', 'responsibles', 'professionals' ])
reversion.register(Modality)
reversion.register(Agreement)
