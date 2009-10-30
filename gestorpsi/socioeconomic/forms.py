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
from gestorpsi.client.models import Transportation, Income, IncomeSource, Possession, Eletricity, PeopleHousehold
from gestorpsi.client.models import Ocuppation, EducationalLevel, Sanitation, Paving, DwellingFeatures
from gestorpsi.person.models import Person
from gestorpsi.client.models import Client
            
class OcuppationForm(models.ModelForm):
    class Meta:
        model = Ocuppation
        fields = ('occupation', 'labor_market_status', 'workplace', 'working_hours', 'comments')

class EducationalLevelForm(models.ModelForm):
    class Meta:
        models = EducationalLevel
        fields = ('school_grade', 'comments')

class TransportationForm(forms.ModelForm):
    class Meta:
        model = Transportation
        fields = ('transportation', 'travel_time', 'comments')

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ('individual_earning', 'household_income', 'comments')

class IncomeSourceForm(forms.ModelForm):
    class Meta:
        model = IncomeSource
        fields = ('income_source', 'comments')

class PossessionForm(forms.ModelForm):
    class Meta:
        model = Possession
        fields = ('item', 'quantity', 'comments')

class EletricityForm(forms.ModelForm):
    class Meta:
        model = Eletricity
        fields = ('eletricity', 'comments')

class SanitationForm(forms.ModelForm):
    class Meta:
        model = Sanitation
        fields = ('water_supply', 'water_treatment', 'sewer', 'waste_disposition' , 'comments')

class PavingForm(forms.ModelForm):
    class Meta:
        model = Paving
        fields = ('paved_street', 'paviment_type', 'comments')

class DwellingFeaturesForm(forms.ModelForm):
    class Meta:
        model = DwellingFeatures
        fields = ('location', 'situation', 'dwelling_type', 'rooms', 'construction_type', 'covering_floor', 'roof_material', 'coating_walls', 'comments')

class PeopleHouseholdForm(forms.ModelForm):
    class Meta:
        model = PeopleHousehold
        fields = ('number_of_people','head_family_edulevel','comments',)

