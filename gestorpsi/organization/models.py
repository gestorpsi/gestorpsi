# -*- coding: utf-8 -*-
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
    description = models.CharField(max_length=30)
    def __unicode__(self):
        """
        returns a representation of this person type as an unicode  C{string}.
        """
        return u"%s" % self.description

class AdministrationType(models.Model):
    """
    This class represents a administration type of Organization. This administration type can be (municipal, state, federal or private)  
    @author: Danilo S. Sanches
    @version: 1.0 
    """
    description = models.CharField(max_length=30)
    def __unicode__(self):
        """
        returns a representation of this administration type as an unicode  C{string}.
        """
        return u"%s" % self.description

class Dependency(models.Model):
    """
    This class represents the organization situation
    @author: Danilo S. Sanches
    @version: 1.0 
    """
    description = models.CharField(max_length=30)
    def __unicode__(self):
        """
        returns a representation of this dependency as an unicode  C{string}.
        """
        return u"%s" % self.description

class FacilityType(models.Model):
    """
    This class represents facility type  
    @author: Danilo S. Sanches
    @version: 1.0 
    """
    description = models.CharField(max_length=100)
    def __unicode__(self):
        """
        returns a representation of this facility type as an unicode  C{string}.
        """
        return u"%s" % self.description

class CareType(models.Model):
    """    
    This class represents a care type provided
    @author: Danilo S. Sanches
    @version: 1.0 
    """
    description = models.CharField(max_length=50)
    def __unicode__(self):
        """
        returns a representation of this care type as an unicode  C{string}.
        """
        return u"%s" % self.description

class Management(models.Model):
    """    
    This class represents a management type of organization 
    @author: Danilo S. Sanches
    @version: 1.0 
    """
    description = models.CharField(max_length=50)
    def __unicode__(self):
        """
        returns a representation of this management as an unicode  C{string}.
        """
        return u"%s" % self.description

class OrganizationType(models.Model):
    """    
    This class represents the organization type
    @author: Danilo S. Sanches
    @version: 1.0 
    """
    description = models.CharField(max_length=50)
    def __unicode__(self):
        """
        returns a representation of this  organization type as an unicode  C{string}.
        """
        return u"%s" % self.description

### it needs more description
class ResearchEducationActivities(models.Model):
    """    
    This class represents the research activities from Organization.  
    @author: Danilo S. Sanches
    @version: 1.0 
    """
    description = models.CharField(max_length=50)
    def __unicode__(self):
        """
        returns a representation of this research activities as an unicode  C{string}.
        """
        return u"%s" % self.description

class Organization(models.Model):
    """    
    This class represents the organization model.   
    @author: Danilo S. Sanches
    @version: 1.0 
    """
    id= UuidField(primary_key=True)
    name = models.CharField(max_length=100)
    businessName = models.CharField(max_length=100, blank=True)
    companyID = models.CharField(max_length=100, blank=True)
    healthCompanyID = models.CharField(max_length=100, blank=True)
    stateTaxID = models.CharField(max_length=30, blank=True)
    cityTaxID = models.CharField(max_length=30, blank=True)
    companyProfessionalLicense = models.CharField(max_length=100, blank=True)
    accountableProfessional = models.CharField(max_length=100, blank=True) 
    
    active = models.BooleanField(default=True)
    icon = models.CharField(max_length=100, blank=True)          
    
    #Profile
    personType = models.OneToOneField(PersonType, null=True, blank=True)
    administrationType = models.OneToOneField(AdministrationType, null=True, blank=True)
    dependency = models.OneToOneField(Dependency, null=True, blank=True)
    facilityType = models.OneToOneField(FacilityType, null=True, blank=True)
    careType = models.OneToOneField(CareType, null=True, blank=True)
    management = models.OneToOneField(Management, null=True, blank=True)
    organizationType = models.OneToOneField(OrganizationType, null=True, blank=True)
    researchEducationActivities = models.OneToOneField(ResearchEducationActivities, null=True, blank=True)
    
    phones = generic.GenericRelation(Phone, null=True)
    address = generic.GenericRelation(Address, null=True)
    emails  = generic.GenericRelation(Email, null=True)
    sites = generic.GenericRelation(Site, null=True)
    instantMessengers =generic.GenericRelation(InstantMessenger, null=True) ### it needs more description    
    organization = models.ForeignKey('self', related_name="%(class)s_related", null=True, blank=True)
    
    # person = models.ForeignKey(Person, null=True)
    # sponsor = models.ForeignKey(Sponsor, null=True)    
    # deviceDetails = models.ForeignKey(DeviceDetails, null=True)
    # employee = models.ForeignKey(Employee, null=True)
    # service = models.ForeignKey(Service, null=True)    
                              
    def __unicode__(self):
        """
        returns a representation of this  organization as an unicode  C{string}.
        """
        return self.name    

"""
from gestorpsi.organization.models import PersonType, AdministrationType, Dependency, FacilityType, CareType, Management, OrganizationType, ResearchEducationActivities, Organization
person_type= PersonType( description= 'person type test' )
person_type.save()

##AdministrationType

admin_type= AdministrationType( description= ' administration type test' )
admin_type.save()

##Dependency
dependency= Dependency( description= 'dependency test' )
dependency.save()

##FacilityType
facility_type= FacilityType( description= 'facility type test')
facility_type.save()

##CareType
care_type= CareType( description= 'care type test' )
care_type.save()

##Management
management= Management(description= 'management test' )
management.save()

##OrganizationType
organization_type= OrganizationType( description= 'organization type test')
organization_type.save()

##ResearchEducationActivities
research_education_activities= ResearchEducationActivities( description= 'research education activities test')
research_education_activities.save()


##Organization
organization= Organization()
organization.name= 'organization test'
organization.bussinessName= 'business name test'
organization.companyID= 9
organization.healthCompanyID= 9
organization.stateTaxID= 9
organization.cityTaxID= 9
organization.companyProfessionalLicense= 'XsDF'
organization.accountableProfessional= 'XsDF'
organization.email= 'organization@test.com.br'
organization.site= 'www.gestorpsi.com.br'
organization.active= True
organization.icon= 'www.google.com.br'
organization.personType= person_type
organization.administrationType= admin_type
organization.dependency= dependency
organization.facilityType= facility_type
organization.careType= care_type
organization.management= management ### it needs more description
organization.organizationType= organization_type
organization.researchEducationActivities= research_education_activities

organization.save()

from gestorpsi.address.models import AddressType, Address, City
from gestorpsi.phone.models import Phone, PhoneType

addressType=AddressType(description='Home')
addressType.save()
address = Address()
address.addressPrefix= 'Rua'
address.addressLine1= 'Rui Barbosa, 1234'
address.addressLine2= 'Anexo II - Sala 4'
address.neighborhood= 'Centro'
address.zipCode= '12345-123'
address.addressType= addressType
address.city= City.objects.get(pk=44085)
address.content_object= organization
address.save()

phoneType= PhoneType( description='Home' )
phoneType.save()
phone = Phone(area='16', phoneNumber='33643223', ext='ttt', phoneType=phoneType)
phone.content_object = organization
phone.save()


address.save()
phone.save()

organization.save()



"""