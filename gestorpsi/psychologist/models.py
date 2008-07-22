from django.db import models
from gestorpsi.careprofessional.models import CareProfessional

class Approaches(models.Model):
    description = models.CharField(max_length=50)
    def __unicode__(self):
        return u"%s" % self.description
    class Admin: pass
    
class Area(models.Model):
    description = models.CharField(max_length=30)
    def __unicode__(self):
        return u"%s" % self.description
    class Admin: pass

class AgeGroup(models.Model):
    description = models.CharField(max_length=30)
    def __unicode__(self):
        return u"%s" % self.description
    class Admin: pass
    
class Psychologist(CareProfessional):
     approaches = models.OneToOneField(Approaches, null=True)
     specialistArea = models.ForeignKey(Area, null=True)
     ageGroup = models.OneToOneField(AgeGroup, null=True)   

     class Admin: pass