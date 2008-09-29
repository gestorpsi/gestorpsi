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
from gestorpsi.organization.models import PersonType, AdministrationType, Dependency
from gestorpsi.organization.models import FacilityType, CareType, Management, OrganizationType
from gestorpsi.organization.models import ResearchEducationActivities, Organization
from gestorpsi.organization.models import Agreement, AgreementType, AgeGroup
from gestorpsi.organization.models import ProcedureProvider, Procedure

class AgeGroupAdmin(admin.ModelAdmin):
    pass

class ProcedureProviderAdmin(admin.ModelAdmin):
    pass

class ProcedureAdmin(admin.ModelAdmin):
    pass

class AgreementAdmin(admin.ModelAdmin):
    pass

class AgreementTypeAdmin(admin.ModelAdmin):
    pass

class PersonTypeAdmin(admin.ModelAdmin):
    pass

class AdministrationTypeAdmin(admin.ModelAdmin):
    pass

class DependencyAdmin(admin.ModelAdmin):
    pass

class FacilityTypeAdmin(admin.ModelAdmin):
    pass

class CareTypeAdmin(admin.ModelAdmin):
    pass

class ManagementAdmin(admin.ModelAdmin):
    pass

class OrganizationTypeAdmin(admin.ModelAdmin):
    pass

class ResearchEducationActivitiesAdmin(admin.ModelAdmin):
    pass

class OrganizationAdmin(admin.ModelAdmin):
    pass

admin.site.register(Agreement, AgreementAdmin)
admin.site.register(AgreementType, AgreementTypeAdmin)
admin.site.register(PersonType, PersonTypeAdmin)
admin.site.register(AdministrationType, AdministrationTypeAdmin)
admin.site.register(Dependency, DependencyAdmin)
admin.site.register(FacilityType, FacilityTypeAdmin)
admin.site.register(CareType, CareTypeAdmin)
admin.site.register(Management, ManagementAdmin)
admin.site.register(OrganizationType, OrganizationTypeAdmin)
admin.site.register(ResearchEducationActivities, ResearchEducationActivitiesAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(AgeGroup, AgeGroupAdmin)
admin.site.register(ProcedureProvider, ProcedureProviderAdmin)
admin.site.register(Procedure, ProcedureAdmin)
