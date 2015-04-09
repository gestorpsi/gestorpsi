# -*- coding: utf-8 -*-

"""
Copyright (C) 2008 GestorPsi

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""

"""
   This file contains all configurations for Admin Interface
   I{These models were created only for testing purposes}
   @author: Sergio Durand
   @version: 1.0
"""
from django.contrib import admin
from gestorpsi.careprofessional.models import PostGraduate, InstitutionType,\
    AcademicResume
from gestorpsi.careprofessional.models import Profession, ProfessionalProfile
from gestorpsi.careprofessional.models import LicenceBoard,\
    ProfessionalIdentification
from gestorpsi.careprofessional.models import CareProfessional
from gestorpsi.careprofessional.models import StudentProfile


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


class StudentProfileAdmin(admin.ModelAdmin):
    pass

admin.site.register(PostGraduate, PostGraduateAdmin)
admin.site.register(InstitutionType, InstitutionTypeAdmin)
admin.site.register(AcademicResume, AcademicResumeAdmin)
admin.site.register(Profession, ProfessionAdmin)
admin.site.register(ProfessionalProfile, ProfessionalProfileAdmin)
admin.site.register(LicenceBoard, LicenceBoardAdmin)
admin.site.register(
    ProfessionalIdentification, ProfessionalIdentificationAdmin)
admin.site.register(CareProfessional, CareProfessionalAdmin)
admin.site.register(StudentProfile, StudentProfileAdmin)
