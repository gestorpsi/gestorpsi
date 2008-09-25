from django.db import models
from django.forms import ModelForm
from django.contrib.contenttypes import generic
from gestorpsi.organization.models import Organization
from gestorpsi.phone.models import Phone
from gestorpsi.address.models import Country, City, Address

# Create your models here.
#gender_list = (('M','Male'),('F','Female'))

#class Establishment(models.Model):
#    name = models.CharField('name',max_length=100)
#    email = models.EmailField('Email')
#    site = models.URLField('site', max_length=50)   
#    phones = generic.GenericRelation(Phone, null=True)
#    address = generic.GenericRelation(Address, null=True)           
     
#    def __unicode__(self):
#        return self.name    
    
#    class Admin:
#        pass
#class EstablishmentForm(ModelForm):
#    class Meta:
#        model= Establishment

#class CareProfessional(models.Model):
#    name = models.CharField('name',max_length=100, core=True)
#    gender = models.CharField(max_length=1, choices=gender_list)        
#    organization = models.ForeignKey(Organization, edit_inline = models.TABULAR, num_in_admin=1)
        
    
    
#    def __unicode__(self):
#        return self.name 
#    
#class CareProfessionalForm(ModelForm):
#    class Meta:
#        model= CareProfessional
       


    
    
   
