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
from gestorpsi.service.models import Area, ServiceType, Modality
from gestorpsi.organization.models import AgeGroup, EducationLevel, HierarchicalLevel

GENERIC_AREA = ('clinic', 'hospital', 'sport', 'forensic', 'legal', 'neuropsyc', 'social', 'traffic', 'psychomotor')
class GenericAreaForm(forms.ModelForm):
    service_type = forms.ModelMultipleChoiceField(label=_("Service Type"), queryset=ServiceType.objects.all(), required=False, widget=forms.Select(attrs={'class':'giant asm'}))
    modalities   = forms.ModelMultipleChoiceField(label=_("Modalities"), queryset=Modality.objects.all(), required=False, widget=forms.SelectMultiple(attrs={'class':'giant multiple asm'}))
    age_group    = forms.ModelMultipleChoiceField(label=_("Age Group"), queryset=AgeGroup.objects.all(), required=False, widget=forms.SelectMultiple(attrs={'class':'giant multiple asm'}))

    class Meta:
        model = Area
        fields = ('service_type', 'modalities', 'age_group')

class SchoolAreaForm(forms.ModelForm):
    service_type    = forms.ModelMultipleChoiceField(label=_("Service Type"), queryset=ServiceType.objects.all(), required=False, widget=forms.Select(attrs={'class':'giant asm'}))
    modalities      = forms.ModelMultipleChoiceField(label=_("Modalities"), queryset=Modality.objects.all(), required=False, widget=forms.SelectMultiple(attrs={'class':'giant multiple asm'}))
    education_level = forms.ModelMultipleChoiceField(label=_("Education Level"), queryset=EducationLevel.objects.all(), required=False, widget=forms.SelectMultiple(attrs={'class':'giant multiple asm'}))
    
    class Meta:
        model = Area
        fields = ('service_type', 'modalities', 'education_level',)

class OrganizationalAreaForm(forms.ModelForm):
    service_type       = forms.ModelMultipleChoiceField(label=_("Service Type"), queryset=ServiceType.objects.all(), required=False, widget=forms.Select(attrs={'class':'giant asm'}))
    modalities         = forms.ModelMultipleChoiceField(label=_("Modalities"), queryset=Modality.objects.all(), required=False, widget=forms.SelectMultiple(attrs={'class':'giant multiple asm'}))
    hierarchical_level = forms.ModelMultipleChoiceField(label=_("Hierarchical Level"), queryset=HierarchicalLevel.objects.all(), required=False, widget=forms.SelectMultiple(attrs={'class':'giant multiple asm'}))
    
    class Meta:
        model = Area
        fields = ('service_type', 'modalities', 'hierarchical_level',)
