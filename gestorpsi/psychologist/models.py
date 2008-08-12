from django.db import models
from django.newforms import ModelForm
from gestorpsi.careprofessional.models import CareProfessional

class Approaches(models.Model):
    description = models.CharField(max_length=50)
    def __unicode__(self):
        return u"%s" % self.description
    class Admin: pass
    
class ApproachesForm(ModelForm):
    class Meta:
        model= Approaches
    
class Area(models.Model):
    description = models.CharField(max_length=30)
    def __unicode__(self):
        return u"%s" % self.description
    class Admin: pass
    
class AreaForm(ModelForm):
    class Meta:
        model= Area

class AgeGroup(models.Model):
    description = models.CharField(max_length=30)
    def __unicode__(self):
        return u"%s" % self.description
    class Admin: pass
    
class AgeGroupForm(ModelForm):
    class Meta:
        model= AgeGroup
    
class Psychologist(CareProfessional):
     approaches = models.OneToOneField(Approaches, null=True)
     specialistArea = models.ForeignKey(Area, null=True)
     ageGroup = models.OneToOneField(AgeGroup, null=True)   

     class Admin: pass
     
class PsychologistForm(ModelForm):
    class Meta:
        model= Psychologist