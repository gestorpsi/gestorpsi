from django.db import models
from django.forms import ModelForm
from django.contrib.contenttypes import generic
from gestorpsi.phone.models import Phone
from gestorpsi.internet.models import Email, Site, InstantMessenger
from gestorpsi.address.models import Country, City, Address
from django.contrib import admin

class PersonType(models.Model):
    description = models.CharField(max_length=30)
    def __unicode__(self):
        return u"%s" % self.description

class PersonTypeAdmin(admin.ModelAdmin):
    pass

admin.site.register(PersonType, PersonTypeAdmin)

class AdministrationType(models.Model):
    description = models.CharField(max_length=30)
    def __unicode__(self):
        return u"%s" % self.description

class AdministrationTypeAdmin(admin.ModelAdmin):
    pass

admin.site.register(AdministrationType, AdministrationTypeAdmin)

class Dependency(models.Model):
    description = models.CharField(max_length=30)
    def __unicode__(self):
        return u"%s" % self.description

class DependencyAdmin(admin.ModelAdmin):
    pass

admin.site.register(Dependency, DependencyAdmin)

class FacilityType(models.Model):
    description = models.CharField(max_length=100)
    def __unicode__(self):
        return u"%s" % self.description

class FacilityTypeAdmin(admin.ModelAdmin):
    pass

admin.site.register(FacilityType, FacilityTypeAdmin)

class CareType(models.Model):
    description = models.CharField(max_length=50)
    def __unicode__(self):
        return u"%s" % self.description

class CareTypeAdmin(admin.ModelAdmin):
    pass

admin.site.register(CareType, CareTypeAdmin)

class Management(models.Model):
    description = models.CharField(max_length=50)
    def __unicode__(self):
        return u"%s" % self.description

class ManagementAdmin(admin.ModelAdmin):
    pass

admin.site.register(Management, ManagementAdmin)
    
class OrganizationType(models.Model):
    description = models.CharField(max_length=50)
    def __unicode__(self):
        return u"%s" % self.description

class OrganizationTypeAdmin(admin.ModelAdmin):
    pass

admin.site.register(OrganizationType, OrganizationTypeAdmin)


class ResearchEducationActivities(models.Model):
    description = models.CharField(max_length=50)
    def __unicode__(self):
        return u"%s" % self.description

class ResearchEducationActivitiesAdmin(admin.ModelAdmin):
    pass

admin.site.register(ResearchEducationActivities, ResearchEducationActivitiesAdmin)


class Organization(models.Model):
    #Identification
    name = models.CharField('name',max_length=100)
    businessName = models.CharField('businessName',max_length=100, null=True, blank=True)
    companyID = models.CharField('companyID',max_length=100, null=True, blank=True)
    healthCompanyID = models.CharField('healthCompanyID',max_length=100, null=True, blank=True)
    stateTaxID = models.CharField('stateTaxID',max_length=30, null=True, blank=True)
    cityTaxID = models.CharField('cityTaxID',max_length=30, null=True, blank=True)
    companyProfessionalLicense = models.CharField('companyProfessionalLicense',max_length=100, null=True, blank=True)
    accountableProfessional = models.CharField('accountableProfessional',max_length=100, null=True, blank=True) 
    email = models.EmailField('email', null=True, blank=True)
    site = models.URLField('site', max_length=50, null=True, blank=True)
    
    active = models.BooleanField(default=True)
    icon = models.CharField('icon', max_length=30,null=True, blank=True)          
    
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
    instantMessengers =generic.GenericRelation(InstantMessenger, null=True)    
    organization = models.ForeignKey('self', related_name="%(class)s_related", null=True, blank=True)
    
    # person = models.ForeignKey(Person, null=True)
    # sponsor = models.ForeignKey(Sponsor, null=True)    
    # deviceDetails = models.ForeignKey(DeviceDetails, null=True)
    # employee = models.ForeignKey(Employee, null=True)
    # service = models.ForeignKey(Service, null=True)    
                              
    def __unicode__(self):
        return self.name    

class OrganizationAdmin(admin.ModelAdmin):
    pass

admin.site.register(Organization, OrganizationAdmin)    


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
organization.management= management
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