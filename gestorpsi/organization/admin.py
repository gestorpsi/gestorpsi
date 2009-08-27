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
from gestorpsi.organization.models import PersonType, UnitType, AdministrationEnvironment, Source, ProvidedType, Management, Dependence, Activitie, Organization, AgreementType, Agreement, AgeGroup, EducationLevel, HierarchicalLevel

admin.site.register(Agreement)
admin.site.register(AgreementType)
admin.site.register(PersonType)
admin.site.register(AdministrationEnvironment)
admin.site.register(Source)
admin.site.register(ProvidedType)
admin.site.register(Management)
admin.site.register(Dependence)
admin.site.register(Activitie)
admin.site.register(UnitType)
admin.site.register(Organization)
admin.site.register(AgeGroup)
admin.site.register(EducationLevel)
admin.site.register(HierarchicalLevel)
