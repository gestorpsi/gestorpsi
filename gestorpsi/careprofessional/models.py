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
from gestorpsi.person.models import Person
from gestorpsi.organization.models import Organization
from gestorpsi.phone.models import Phone
from gestorpsi.place.models import Place
from gestorpsi.address.models import Country, City, Address
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from gestorpsi.util.uuid_field import UuidField
from gestorpsi.util import audittrail
from gestorpsi.organization.models import Agreement

class InstitutionType(models.Model):
    """    
    This class represents an institution type.   
    @author: Danilo S. Sanches
    @version: 1.0 
    """
    description = models.CharField(max_length=50, null=True)
    def __unicode__(self):
        """
        returns a representation of this Institution type as an unicode  C{string}.
        """
        return u"%s" % self.description

class PostGraduate(models.Model):
    """    
    An instance of this class represents the postgraduate of careprofessional. This instance is relation on with careprofessional's academic resume      
    @author: Danilo S. Sanches
    @version: 1.0 
    """
    description = models.CharField(max_length=50, null=True)
    def __unicode__(self):
        """
        returns a representation of this  PostGraduate as an unicode  C{string}.
        """
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

class Profession(models.Model):
    """    
    This class represents the careprofessional's profession       
    @author: Danilo S. Sanches
    @version: 1.0 
    """
    number = models.CharField(max_length=20, null=True)
    description = models.CharField(max_length=50, null=True)
    def __unicode__(self):
        """
        returns a representation of this Profession as an unicode  C{string}.
        """
        return u"%s" % self.description

#class Agreement(models.Model):
#    """
#    This class represents an agreement type that the careprofessional works
#    @author: Danilo S. Sanches
#    @version: 1.0
#    """
#    description = models.CharField(max_length=50, null=True)
#    def __unicode__(self):
#        """
#        returns a representation of this Agreement as an unicode  C{string}.
#        """
#        return u"%s" % self.description

class ProfessionalProfile(models.Model):
    """
    This class represents the professional profile
    @author: Danilo S. Sanches
    @version: 1.0
    """
    id= UuidField( primary_key= True )
    academicResume = models.OneToOneField(AcademicResume, null=True)
    initialProfessionalActivities = models.CharField(max_length=10, null=True)
    agreement = models.ManyToManyField(Agreement, null=True)
    profession = models.OneToOneField(Profession, null=True)
    services = models.CharField(max_length=100, null=True)
    availableTime = models.CharField(max_length=100, null=True)
    workplace = models.ManyToManyField(Place, null=True)
    
    def __unicode__(self):
        """
        returns a representation of this professional profile as an unicode  C{string}.
        """
        return "initial professional activities= %s; agreements= %s" % ( self.initialProfessionalActivities, self.agreement.all() )

class LicenceBoard(models.Model):
    """
    This class represents the careprofessional's licence board
    @author: Danilo S. Sanches
    @version: 1.0
    """
    name = models.CharField(max_length=20, null=True)
    description = models.CharField(max_length=100, null=True)
    
    def __unicode__(self):
        """
        returns a representation of this licence board as an unicode  C{string}.
        """
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
        """
        returns a representation of this professional identification as an unicode  C{string}.
        """
        return self.registerNumber

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
    
    history= audittrail.AuditTrail()
    
    def __unicode__(self):
        return u"%s" % self.person    

"""
from gestorpsi.address.models import Country
from gestorpsi.person.models import Person
from gestorpsi.organization.models import Organization
from gestorpsi.careprofessional.models import InstitutionType, PostGraduate, AcademicResume, Profession, ProfessionalProfile, LicenceBoard, ProfessionalIdentification, CareProfessional
from gestorpsi.address.models import Country, State, City, Address, AddressType
from gestorpsi.phone.models import Phone, PhoneType

person= Person()
person.name='jose silva'
person.lastname='pereira'
person.nationality = Country.objects.get(pk=33)
person.save()

instType = InstitutionType( description='testInstitution')
instType.save()

postGraduate = PostGraduate( description='posGraduateTest')
postGraduate.save()

resume = AcademicResume()
resume.teachingInstitute = 'UFSCar'
resume.institutionType = instType
resume.course = 'testCourse'
resume.initialDateGraduation = '2000-10-01'
resume.finalDateGraduation = '2005-10-01'
resume.lattesResume = 'http://www.gestorpsi.com.br'
resume.postGraduate = postGraduate
resume.initialDatePostGraduate = '2006-03-01'
resume.finalDatePostGraduate = '2008-03-01'
resume.area = 'testArea'
resume.save()

addressType=AddressType(description='Home')
addressType.save()

address = Address()
address.addressPrefix = 'Rua'
address.addressLine1 = 'Rui Barbosa, 1234'
address.addressLine2 = 'Anexo II - Sala 4'
address.neighborhood = 'Centro'
address.zipCode = '12345-123'
address.addressType = addressType
address.city = City.objects.get(pk=44218)
address.save()

phoneType = PhoneType( description='Home' )
phoneType.save()
phone = Phone(area='16', phoneNumber='33643223', ext='ttt', phoneType=phoneType)
phone.save()

profession = Profession(number='10', description='Psicologo')
profession.save()

agreement = Agreement(description='Unimed')
agreement.save()

profile = ProfessionalProfile()
profile.academicResume = AcademicResume.objects.get(pk=1)
profile.initialPrifessionalActivities = '10/2000'
profile.agreement = Agreement.objects.get(pk=1)
profile.profession = Profession.objects.get(pk=1)
profile.services = 'Psicanalise'
profile.availableTime = '30 horas semanais'
profile.save()

licence = LicenceBoard(name='CRRT' ,description='testtt')
licence.save()

identification = ProfessionalIdentification(registerNumber='111', licenceBoard = LicenceBoard.objects.get(pk=1))
identification.save()

care = CareProfessional()
care.professionalIdentification = ProfessionalIdentification.objects.get(pk=1)
care.professionalProfile = ProfessionalProfile.objects.get(pk=1)
care.person = Person.objects.get(pk=1)
care.comments = 'ate que enfim!!!'
care.save()
"""
