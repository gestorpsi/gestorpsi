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
from gestorpsi.service.models import Service, ResearchProject, Area, Modality, ServiceType, Clinic

class AreaInline(admin.TabularInline):
    model = ServiceType

class ServiceAdmin(admin.ModelAdmin):
    pass

class ResearchProjectAdmin(admin.ModelAdmin):
    pass

class AreaAdmin(admin.ModelAdmin):
    inlines = [AreaInline]
    pass



admin.site.register(Service, ServiceAdmin)
admin.site.register(ResearchProject, ResearchProjectAdmin)
admin.site.register(Area, AreaAdmin)
admin.site.register(Modality)
admin.site.register(ServiceType)
admin.site.register(Clinic)