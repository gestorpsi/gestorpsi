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

from django import forms
from django.utils.translation import ugettext as _

from gestorpsi.service.models import Service, ServiceGroup, Area, ServiceType, Modality
from gestorpsi.client.models import Client
from gestorpsi.organization.models import AgeGroup, EducationLevel, HierarchicalLevel

GENERIC_AREA = ('clinic', 'hospital', 'sport', 'forensic', 'legal', 'neuropsyc', 'social', 'traffic', 'psychomotor')
class GenericAreaForm(forms.ModelForm):
    service_type = forms.ModelMultipleChoiceField(label=_("Service Type"), queryset=ServiceType.objects.all(), required=False, widget=forms.Select(attrs={'class':'giant asm'}))
    modalities   = forms.ModelMultipleChoiceField(label=_("Modalities"), queryset=Modality.objects.all(), required=False, widget=forms.CheckboxSelectMultiple())
    age_group    = forms.ModelMultipleChoiceField(label=_("Age Group"), queryset=AgeGroup.objects.all(), required=False, widget=forms.CheckboxSelectMultiple())

    class Meta:
        model = Area
        fields = ('service_type', 'modalities', 'age_group')

class SchoolAreaForm(forms.ModelForm):
    service_type    = forms.ModelMultipleChoiceField(label=_("Service Type"), queryset=ServiceType.objects.all(), required=False, widget=forms.Select(attrs={'class':'giant asm'}))
    modalities      = forms.ModelMultipleChoiceField(label=_("Modalities"), queryset=Modality.objects.all(), required=False, widget=forms.CheckboxSelectMultiple())
    education_level = forms.ModelMultipleChoiceField(label=_("Education Level"), queryset=EducationLevel.objects.all(), required=False, widget=forms.CheckboxSelectMultiple())
    
    class Meta:
        model = Area
        fields = ('service_type', 'modalities', 'education_level',)

class OrganizationalAreaForm(forms.ModelForm):
    service_type       = forms.ModelMultipleChoiceField(label=_("Service Type"), queryset=ServiceType.objects.all(), required=False, widget=forms.Select(attrs={'class':'giant asm'}))
    modalities         = forms.ModelMultipleChoiceField(label=_("Modalities"), queryset=Modality.objects.all(), required=False, widget=forms.CheckboxSelectMultiple())
    hierarchical_level = forms.ModelMultipleChoiceField(label=_("Hierarchical Level"), queryset=HierarchicalLevel.objects.all(), required=False, widget=forms.CheckboxSelectMultiple())
    
    class Meta:
        model = Area
        fields = ('service_type', 'modalities', 'hierarchical_level',)

class ServiceGroupForm(forms.ModelForm):
    description = forms.CharField(widget=forms.TextInput(attrs={'class':'giant', }))
    comments = forms.CharField(widget=forms.Textarea(attrs={'class':'giant', }), required = False)

    class Meta:
        fields = ('description','comments','active')
        model = ServiceGroup
