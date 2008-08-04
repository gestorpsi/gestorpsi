from django.db import models
from gestorpsi.person.models import Person
from gestorpsi.organization.models import Organization
from gestorpsi.phone.models import Phone
from gestorpsi.address.models import Country, City, Address
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic


class InstitutionType(models.Model):
    description = models.CharField(max_length=50, null=True)
    def __unicode__(self):
        return u"%s" % self.description
    class Admin: pass
    
class PostGraduate(models.Model):
    description = models.CharField(max_length=50, null=True)
    def __unicode__(self):
        return u"%s" % self.description
    class Admin: pass

class AcademicResume(models.Model):
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
    
    class Admin: 
        pass


class WorkPlaces(models.Model):
    name = models.CharField(max_length=30, null=True)
    phones = generic.GenericRelation(Phone, null=True)
    address = generic.GenericRelation(Address, null=True)
    
    def __unicode__(self):
        return u"%s" % self.name
    
    class Admin:
        pass

class Profession(models.Model):
    number = models.CharField(max_length=20, null=True)
    description = models.CharField(max_length=50, null=True)
    def __unicode__(self):
        return u"%s" % self.description
    class Admin: pass


class Agreement(models.Model):
    description = models.CharField(max_length=50, null=True)
    def __unicode__(self):
        return u"%s" % self.description
    class Admin: pass
    

class ProfessionalProfile(models.Model):
    academicResume = models.OneToOneField(AcademicResume, null=True)
    initialPrifessionalActivities = models.CharField(max_length=10, null=True)
    agreement = models.ForeignKey(Agreement, null=True)
    profession = models.OneToOneField(Profession, null=True)
    services = models.CharField(max_length=100, null=True)
    availableTime = models.CharField(max_length=100, null=True)
    workplace = models.ForeignKey(WorkPlaces, null=True)
    
    class Admin: 
        pass


class LicenceBoard(models.Model):
    name = models.CharField('name',max_length=20, core=True)
    description = models.CharField('description',max_length=100, core=True)
    
    def __unicode__(self):
        return self.name
    
    class Admin:
        pass

class ProfessionalIdentification(models.Model):
    licenceBoard = models.ForeignKey(LicenceBoard, edit_inline = models.TABULAR, num_in_admin=1)
    registerNumber = models.CharField('registerNumber',max_length=50, core=True)    
    
    def __unicode__(self):
        return self.registerNumber
    
    class Admin:
        pass
     
class CareProfessional(models.Model):
    professionalIdentification = models.ForeignKey(ProfessionalIdentification, edit_inline = models.TABULAR, num_in_admin=1, core=True, null=True)
    professionalProfile = models.ForeignKey(ProfessionalProfile, edit_inline = models.TABULAR, num_in_admin=1, core=True, null = True)
    person = models.OneToOneField(Person)
    comments = models.CharField('comments',max_length=200, core=True, null=True)
    
        
    class Admin:
       pass
    