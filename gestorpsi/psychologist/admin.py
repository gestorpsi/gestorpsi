# -*- coding: utf-8 -*-
"""
   This file contains all configurations for Admin Interface
   I{These models were created only for testing purposes}
   @author: Sergio Durand
   @version: 1.0
"""

from django.contrib import admin
from gestorpsi.psychologist.models import Approaches, Area, AgeGroup, Psychologist

class ApproachesAdmin(admin.ModelAdmin):
    pass

class AreaAdmin(admin.ModelAdmin):
    pass

class AgeGroupAdmin(admin.ModelAdmin):
    pass

class PsychologistAdmin(admin.ModelAdmin):
    pass

admin.site.register(Approaches, ApproachesAdmin)
admin.site.register(Area, AreaAdmin)
admin.site.register(AgeGroup, AgeGroupAdmin)
admin.site.register(Psychologist, PsychologistAdmin)