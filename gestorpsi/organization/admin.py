# -*- coding: utf-8 -*-
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
from gestorpsi.organization.models import Agreement, AgreementType

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