from django.db import models
from django.forms import ModelForm
from gestorpsi.careprofessional.models import CareProfessional
from django.contrib import admin

class Approaches(models.Model):
    description = models.CharField(max_length=50)
    def __unicode__(self):
        return u"%s" % self.description

class ApproachesAdmin(admin.ModelAdmin):
    pass

admin.site.register(Approaches, ApproachesAdmin)

    
class ApproachesForm(ModelForm):
    class Meta:
        model= Approaches
    
class Area(models.Model):
    description = models.CharField(max_length=30)
    def __unicode__(self):
        return u"%s" % self.description

class AreaAdmin(admin.ModelAdmin):
    pass

admin.site.register(Area, AreaAdmin)
    
class AreaForm(ModelForm):
    class Meta:
        model= Area

class AgeGroup(models.Model):
    description = models.CharField(max_length=30)
    def __unicode__(self):
        return u"%s" % self.description

class AgeGroupAdmin(admin.ModelAdmin):
    pass

admin.site.register(AgeGroup, AgeGroupAdmin)

    
class AgeGroupForm(ModelForm):
    class Meta:
        model= AgeGroup
    
class Psychologist(CareProfessional):
     approaches = models.OneToOneField(Approaches, null=True)
     specialistArea = models.ForeignKey(Area, null=True)
     ageGroup = models.OneToOneField(AgeGroup, null=True)   

class PsychologistAdmin(admin.ModelAdmin):
    pass

admin.site.register(Psychologist, PsychologistAdmin)
     
class PsychologistForm(ModelForm):
    class Meta:
        model= Psychologist