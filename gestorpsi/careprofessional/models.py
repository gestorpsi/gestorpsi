from django.db import models
from gestorpsi.person.models import Person
from gestorpsi.organization.models import Organization
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

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
    comments = models.CharField('comments',max_length=200, core=True)
    
    def __unicode__(self):
        return self.registerNumber
    
    class Admin:
        pass
    
class CareProfessional(Person):
    professionalIdentification = models.ForeignKey(ProfessionalIdentification, edit_inline = models.TABULAR, num_in_admin=1, core=True)
    org = models.ManyToManyField(Organization)
     
     # Generic Relationship
    #content_type = models.ForeignKey(ContentType)
    #object_id = models.PositiveIntegerField()
    #content_object = generic.GenericForeignKey()    
    