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
from gestorpsi.organization.models import PersonType, UnitType, AdministrationEnvironment, Source, ProvidedType, Management, Dependence, Activitie, Organization, AgreementType, Agreement, AgeGroup, ProcedureProvider, Procedure

class AgeGroupAdmin(admin.ModelAdmin):
    pass

class PersonTypeAdmin(admin.ModelAdmin):
    pass

class UnitTypeAdmin(admin.ModelAdmin):
    pass

class AdministrationEnvironmentAdmin(admin.ModelAdmin):
    pass

class AgreementAdmin(admin.ModelAdmin):
    pass

class AgreementTypeAdmin(admin.ModelAdmin):
    pass

class SourceAdmin(admin.ModelAdmin):
    pass

class ProvidedTypeAdmin(admin.ModelAdmin):
    pass

class ManagementAdmin(admin.ModelAdmin):
    pass

class DependenceAdmin(admin.ModelAdmin):
    pass

class ActivitieAdmin(admin.ModelAdmin):
    pass

class ManagementAdmin(admin.ModelAdmin):
    pass

class ProcedureProviderAdmin(admin.ModelAdmin):
    pass

class ProcedureAdmin(admin.ModelAdmin):
    pass

class OrganizationAdmin(admin.ModelAdmin):
    pass

admin.site.register(Agreement, AgreementAdmin)
admin.site.register(AgreementType, AgreementTypeAdmin)
admin.site.register(PersonType, PersonTypeAdmin)
admin.site.register(AdministrationEnvironment, AdministrationEnvironmentAdmin)
admin.site.register(Source, SourceAdmin)
admin.site.register(ProvidedType, ProvidedTypeAdmin)
admin.site.register(Management, ManagementAdmin)
admin.site.register(Dependence, DependenceAdmin)
admin.site.register(Activitie, ActivitieAdmin)
admin.site.register(UnitType, UnitTypeAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(AgeGroup, AgeGroupAdmin)
admin.site.register(ProcedureProvider, ProcedureProviderAdmin)
admin.site.register(Procedure, ProcedureAdmin)

