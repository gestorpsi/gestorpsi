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

from django import forms
from django.contrib import admin
from django.db.models import Q


from gestorpsi.organization.models import *
from gestorpsi.person.models import Person


class ProfessionalResponsibleForm(forms.ModelForm):
    pass
    #model = ProfessionalResponsible

    #def __init__(self, *args, **kwargs):
        #super(ProfessionalResponsibleForm, self).__init__(*args, **kwargs)
        
        ##query = Q(professionalresponsible=None) & Q(professionalresponsible__organization=None)
        #query = Q(professionalresponsible__organization=None)
        #try:
            #temp = self.instance.person.pk
            #query |= Q(pk__exact = temp)
        #except:
            #pass
        #query = Person.objects.filter(query)
        
        #self.fields['person'].queryset = query


class ProfessionalResponsibleInline(admin.StackedInline):
    form = ProfessionalResponsibleForm
    model = ProfessionalResponsible
    extra = 1


'''
    organization filter and action
'''
def turnoff(modeladmin, request, queryset):
        for obj in queryset:
            obj.active = False
            obj.save()
turnoff.short_description = "Desativar organização"

def turnon(modeladmin, request, queryset):
        for obj in queryset:
            obj.active = True
            obj.save()
turnon.short_description = "Ativar organização"

class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name','id','active','suspension','trade_name','short_name')
    list_filter = ['active',]
    search_fields = ['name','trade_name','short_name','id']
    actions = [turnoff, turnon]


class ProfessionalResponsibleAdmin(admin.ModelAdmin):
    form = ProfessionalResponsibleForm


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
admin.site.register(AgeGroup)
admin.site.register(EducationLevel)
admin.site.register(HierarchicalLevel)
admin.site.register(ProfessionalResponsible, ProfessionalResponsibleAdmin)
admin.site.register(Organization, OrganizationAdmin)
