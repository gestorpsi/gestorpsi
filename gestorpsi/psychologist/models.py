from django.db import models
from django.forms import ModelForm
from gestorpsi.careprofessional.models import CareProfessional
from django.contrib import admin

class Approaches(models.Model):
    """
    Represents the necessary approaches (theoric reference) for psychologist
    @version: 1.0  
    """    
    description = models.CharField(max_length=50)
    def __unicode__(self):
        """
        returns the attribute as unicode C{string}
        """
        return u"%s" % self.description

class ApproachesAdmin(admin.ModelAdmin):
    pass

admin.site.register(Approaches, ApproachesAdmin)

    
class ApproachesForm(ModelForm):
    class Meta:
        model= Approaches
    
class Area(models.Model):
    """
    Represents psychologist's specialist area
    @version: 1.0 
    """
    description = models.CharField(max_length=30)
    def __unicode__(self):
        """
        returns the attribute as unicode C{string}
        """
        return u"%s" % self.description

class AreaAdmin(admin.ModelAdmin):
    pass

admin.site.register(Area, AreaAdmin)
    
class AreaForm(ModelForm):
    class Meta:
        model= Area

class AgeGroup(models.Model):
    """
    This class represents the AgeGroup that psychologist works
    @version: 1.0  
    """
    description = models.CharField(max_length=30)
    def __unicode__(self):
        """
        returns the attribute as unicode C{string}
        """
        return u"%s" % self.description

class AgeGroupAdmin(admin.ModelAdmin):
    pass

admin.site.register(AgeGroup, AgeGroupAdmin)

    
class AgeGroupForm(ModelForm):
    class Meta:
        model= AgeGroup
    
class Psychologist(CareProfessional):
     
     """
     This class represents a psychologist model. This  model needs some fields from CareProfessional and for this, an inherit from CareProfessional was used.        
     @author: Danilo S. Sanches
     @version: 1.0
     @see: CareProfessional
     """
     approaches = models.OneToOneField(Approaches, null=True)
     specialistArea = models.ForeignKey(Area, null=True)
     ageGroup = models.OneToOneField(AgeGroup, null=True)   

class PsychologistAdmin(admin.ModelAdmin):
    pass

admin.site.register(Psychologist, PsychologistAdmin)
     
class PsychologistForm(ModelForm):
    class Meta:
        model= Psychologist