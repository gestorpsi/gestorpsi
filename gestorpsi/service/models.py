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
from gestorpsi.organization.models import Organization
from gestorpsi.careprofessional.models import CareProfessional
from django.forms import ModelForm
from gestorpsi.util.uuid_field import UuidField
from gestorpsi.organization.models import Agreement

class ServiceType(models.Model):
    """
    This class holds information on available service types.
    @author: Vinicius H. S. Durelli
    @version: 1.0
    """
    name= models.CharField( max_length= 80 )
    description= models.CharField( max_length= 100 )

PROCEDURE_LIST= ( ( '1', 'SUS'), ( '2', 'CFP'), ( '3', 'GESTORPSI') )    
class Procedure(models.Model):
    """
    This class represents a procedure.
    @author: Vinicius H. S. Durelli
    @version: 1.0
    """
    id_proc= models.CharField( max_length= 20, blank= True )
    name= models.CharField( max_length= 80 )
    description= models.CharField( max_length= 80, blank= True )
    type= models.CharField( max_length= 1, choices= PROCEDURE_LIST )

class Modality(models.Model):
    """
    Instances of this class are created to represent modalities. Modalities have a name and a description.
    @author: Vinicius H. S. Durelli
    @version: 1.0
    """
    name= models.CharField( max_length= 80 )
    description= models.CharField( max_length= 100 )
    
class GenericArea(models.Model):
    """
    C{GenericArea} holds ordinary information on areas. Instances of this class should not be instantiated, this class is used only
    to provide a general structure that is inherited by its subclasses.
    @author: Vinicius H. S. Durelli
    @version: 1.0
    """
    services= models.ManyToManyField( ServiceType )
    modalities= models.ManyToManyField( Modality )
    procedures= models.ManyToManyField( Procedure )

class School(GenericArea):
    education_modality= models.CharField( max_length= 80 )

class Organizational(GenericArea):
    hierarchical_level= models.CharField( max_length= 80 )

class Clinic(GenericArea):
    #FAIXA ETARIA
    pass


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
    id= UuidField(primary_key=True)
    name= models.CharField( max_length= 80 )
    description= models.CharField( max_length= 100 )
    keywords= models.CharField( max_length= 100 )
    agreements= models.ManyToManyField( Agreement )
    research_project= models.ForeignKey( ResearchProject, null=True )    
    organization = models.ForeignKey(Organization, null=True)
    active= models.BooleanField(default=True)
    organization= models.ForeignKey(Organization, null=True)
    responsibles= models.ManyToManyField( CareProfessional )
        
    def __unicode__(self):
        return u"%s" % (self.name)

class ServiceForm(ModelForm):
    class Meta:
        model= Service

"""

from gestorpsi.service.models import ResearchProject
research_project= ResearchProject( name= 'a research project', description= 'research project test' )
research_project.save()

from gestorpsi.service.models import AgreementType
agreement_type= AgreementType( description= 'agreement type test' )
agreement_type.save()


from gestorpsi.service.models import Agreement
agreement= Agreement( name= 'an agreement', description= 'agreement test', agreement_type= agreement_type )
agreement.save()

from gestorpsi.service.models import Service
from gestorpsi.organization.models import Organization
from gestorpsi.careprofessional.models import CareProfessional
service= Service()
service.name= 'service test'
service.description= 'service description'
service.keywords= 'some keywords: Java, Ruby and Python'
service.research_project= research_project
service.organization= Organization.objects.get(pk=1)
service.save()

service.agreements.add( agreement )
service.responsibles.add( CareProfessional.objects.get(pk=1) )
service.save()
"""
