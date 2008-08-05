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
    

"""
from gestorpsi.address.models import Country
from gestorpsi.person.models import Person
from gestorpsi.organization.models import Organization
from gestorpsi.careprofessional.models import InstitutionType, PostGraduate, AcademicResume, WorkPlaces, Profession, Agreement, ProfessionalProfile, LicenceBoard, ProfessionalIdentification, CareProfessional
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
resume.institutionType = InstitutionType.objects.get(pk=1)
resume.course = 'testCourse'
resume.initialDateGraduation = '2000-10-01'
resume.finalDateGraduation = '2005-10-01'
resume.lattesResume = 'http://www.gestorpsi.com.br'
resume.postGraduate = PostGraduate.objects.get(pk=1)
resume.initialDatePostGraduate = '2006-03-01'
resume.finalDatePostGraduate = '2008-03-01'
resume.area = 'testArea'
resume.save()

workPlaces = WorkPlaces()
workPlaces.name='Instituto de Psicologia'
workPlaces.save()

addressType=AddressType(description='Home')
addressType.save()
address = Address()
address.addressPrefix = 'Rua'
address.addressLine1 = 'Rui Barbosa, 1234'
address.addressLine2 = 'Anexo II - Sala 4'
address.neighborhood = 'Centro'
address.zipCode = '12345-123'
address.addressType = AddressType.objects.get(pk=1)
address.city = City.objects.get(pk=44085)
address.content_object = WorkPlaces.objects.get(pk=1)
address.save()

phoneType = PhoneType( description='Home' )
phoneType.save()
phone = Phone(area='16', phoneNumber='33643223', ext='ttt', phoneType=PhoneType.objects.get(pk=1))
phone.content_object = WorkPlaces.objects.get(pk=1)
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
profile.workplace = WorkPlaces.objects.get(pk=1)
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
