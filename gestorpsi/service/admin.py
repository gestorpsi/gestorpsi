# -*- coding: utf-8 -*-
"""
   This file contains all configurations for Admin Interface
   I{These models were created only for testing purposes}
   @author: Sergio Durand
   @version: 1.0
"""

from django.contrib import admin
from gestorpsi.service.models import Service, ResearchProject, Agreement, AgreementType

class ServiceAdmin(admin.ModelAdmin):
    pass

class ResearchProjectAdmin(admin.ModelAdmin):
    pass

class AgreementAdmin(admin.ModelAdmin):
    pass

class AgreementTypeAdmin(admin.ModelAdmin):
    pass

admin.site.register(Service, ServiceAdmin)
admin.site.register(ResearchProject, ResearchProjectAdmin)
admin.site.register(Agreement, AgreementAdmin)
admin.site.register(AgreementType, AgreementTypeAdmin)