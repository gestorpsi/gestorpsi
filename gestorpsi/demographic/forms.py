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
from gestorpsi.demographic.models import Profession, EducationalLevel
from gestorpsi.demographic.choices import *
from gestorpsi.cbo.models import Occupation

class ProfessionForm(forms.ModelForm):
    profession = forms.ModelChoiceField(queryset=Occupation.objects.all(), widget=forms.Select(attrs={'class':'giant asm'}))
    labor_market_status = forms.ChoiceField(choices=LABOR_MARKET_STATUS, widget=forms.Select(attrs={'class':'giant asm'}))
    workplace = forms.CharField(required=False, widget=forms.Textarea(attrs={'class':'giant asm'}))
    working_hours = forms.CharField(required=False, widget=forms.Textarea(attrs={'class':'giant asm'}))
    comments = forms.CharField(required=False, widget=forms.Textarea(attrs={'class':'giant asm'}))
    status = forms.BooleanField(required=False, help_text=_("Still active in this occupation"))
    class Meta:
        model = Profession
        fields = ('profession','labor_market_status', 'workplace', 'working_hours', 'comments', 'status')

class EducationalLevelForm(forms.ModelForm):
    school_grade = forms.ChoiceField(choices=EDUCATION_LEVEL, widget=forms.Select(attrs={'class':'giant asm'}))
    comments = forms.CharField(required=False, widget=forms.Textarea(attrs={'class':'giant asm'}))
    class Meta:
        model = EducationalLevel
        fields = ('school_grade','comments')
