# -*- coding: utf-8 -*-
"""
   This file contains all configurations for Admin Interface
   I{These models were created only for testing purposes}
   @author: Sergio Durand
   @version: 1.0
"""
from django.contrib import admin
from gestorpsi.careprofessional.models import PostGraduate, InstitutionType, AcademicResume
from gestorpsi.careprofessional.models import Profession, ProfessionalProfile
from gestorpsi.careprofessional.models import LicenceBoard, ProfessionalIdentification
from gestorpsi.careprofessional.models import CareProfessional
from gestorpsi.organization.models import Agreement

class InstitutionTypeAdmin(admin.ModelAdmin):
    pass

class PostGraduateAdmin(admin.ModelAdmin):
    pass

class AcademicResumeAdmin(admin.ModelAdmin):
    pass

class ProfessionAdmin(admin.ModelAdmin):
    pass

class ProfessionalProfileAdmin(admin.ModelAdmin):
    pass

class LicenceBoardAdmin(admin.ModelAdmin):
    pass

class ProfessionalIdentificationAdmin(admin.ModelAdmin):
    pass

class CareProfessionalAdmin(admin.ModelAdmin):
    pass

admin.site.register(PostGraduate, PostGraduateAdmin)
admin.site.register(InstitutionType, InstitutionTypeAdmin)
admin.site.register(AcademicResume, AcademicResumeAdmin)
admin.site.register(Profession, ProfessionAdmin)
admin.site.register(ProfessionalProfile, ProfessionalProfileAdmin)
admin.site.register(LicenceBoard, LicenceBoardAdmin)
admin.site.register(ProfessionalIdentification, ProfessionalIdentificationAdmin)
admin.site.register(CareProfessional, CareProfessionalAdmin)