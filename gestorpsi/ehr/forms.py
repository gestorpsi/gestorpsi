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
from gestorpsi.ehr.models import TimeUnit, Diagnosis, Demand, Session, SESSION_GOALS, DEMAND_STATUS, DIAGNOSIS_STATUS, DIAGNOSIS_STATUS2, SEVERITY, UNITS
from gestorpsi.schedule.models import ScheduleOccurrence

class TimeUnitForm(forms.ModelForm):
    unit = forms.CharField(label=_('Unit'), required=False, widget=forms.TextInput(attrs={'class':'medium asm'}))
    time = forms.ChoiceField(choices=UNITS, label=_('Time'), widget=forms.Select(attrs={'class':'medium asm'}))
    class Meta:
        model = TimeUnit
        fields = ('unit','time')

class DemandForm(forms.ModelForm):
    occurrence = forms.ModelChoiceField(queryset=ScheduleOccurrence.objects.all(), required=False, label=_('Occurence'), widget=forms.Select(attrs={'class':'giant asm'}))
    initial_complaint = forms.BooleanField(label=_('Initial complaint'), required=False, widget=forms.CheckboxInput)
    demand = forms.CharField(label=_('Demand'), required=True, widget=forms.TextInput(attrs={'class':'giant asm'}))
    description = forms.CharField(label=_('Description'), required=False, widget=forms.Textarea(attrs={'class':'giant asm'}))
    severity = forms.ChoiceField(choices=SEVERITY, label=_('Severity'), widget=forms.Select(attrs={'class':'giant asm'}))
    demand_status = forms.ChoiceField(choices=DEMAND_STATUS, label=_('Demand status'), widget=forms.Select(attrs={'class':'giant asm'}))
    demand_resolution = forms.DateField(label=_('Demand resolution'), required=False, input_formats=('%d/%m/%Y',), widget=forms.DateInput(attrs={'class':'giant asm', 'mask':'99/99/9999'}, format='%d/%m/%Y'))
    bibliography = forms.CharField(label=_('Bibliography'), required=False, widget=forms.Textarea(attrs={'class':'giant asm'}))
    related_sites = forms.CharField(label=_('Related Sites'), required=False, widget=forms.Textarea(attrs={'class':'giant asm'}))
    comments = forms.CharField(label=_('Comments'), required=False, widget=forms.Textarea(attrs={'class':'giant asm'}))
    class Meta:
        model = Demand
        fields = ('occurrence','initial_complaint','demand','description','severity','demand_status','demand_resolution','bibliography','related_sites','comments')

class DiagnosisForm(forms.ModelForm):
    occurrence = forms.ModelChoiceField(queryset=ScheduleOccurrence.objects.all(), required=False, label=_('Occurence'), widget=forms.Select(attrs={'class':'giant asm'}))
    diagnosis_date = forms.DateField(label=_('Diagnosis Date'), required=False, input_formats=('%d/%m/%Y',), widget=forms.DateInput(attrs={'class':'giant asm', 'mask':'99/99/9999'}, format='%d/%m/%Y'))
    diagnosis_resolution = forms.DateField(label=_('Diagnosis Resolution Date'), required=False, input_formats=('%d/%m/%Y',), widget=forms.DateInput(attrs={'class':'giant asm', 'mask':'99/99/9999'}, format='%d/%m/%Y'))
    diagnosis = forms.CharField(label=_('Diagnosis'), required=True, widget=forms.TextInput(attrs={'class':'giant asm'}))
    diagnosis_status = forms.ChoiceField(choices=DIAGNOSIS_STATUS, label=_('Diagnosis Status'), widget=forms.Select(attrs={'class':'giant asm'}))
    diagnosis_status2 = forms.ChoiceField(choices=DIAGNOSIS_STATUS2, label='', widget=forms.Select(attrs={'class':'giant asm'}))
    clinical_description = forms.CharField(label=_('Clinical Description'), required=False, widget=forms.Textarea(attrs={'class':'giant asm'}))
    severity = forms.ChoiceField(choices=SEVERITY, label=_('Severity'), widget=forms.Select(attrs={'class':'giant asm'}))
    treatment_indicated = forms.CharField(label=_('Treatment Indicated'), required=False, widget=forms.Textarea(attrs={'class':'giant asm'}))
    bibliography = forms.CharField(label=_('Bibliography'), required=False, widget=forms.Textarea(attrs={'class':'giant asm'}))
    related_sites = forms.CharField(label=_('Related Sites'), required=False, widget=forms.Textarea(attrs={'class':'giant asm'}))
    comments = forms.CharField(label=_('Comments'), required=False, widget=forms.Textarea(attrs={'class':'giant asm'}))
    class Meta:
        model = Diagnosis
        fields = ('occurrence', 'diagnosis_date', 'diagnosis_resolution', 'diagnosis', 'diagnosis_status', 'diagnosis_status2', 'clinical_description', 'severity', 'treatment_indicated', 'bibliography', 'related_sites', 'comments')

class SessionForm(forms.ModelForm):
    occurrence = forms.ModelChoiceField(queryset=ScheduleOccurrence.objects.all(), label=_('Occurence'), widget=forms.Select(attrs={'class':'giant asm'}))
    session_goals = forms.ChoiceField(choices=SESSION_GOALS, label=_('Session Goals'), widget=forms.Select(attrs={'class':'giant asm'}))
    descriptive = forms.CharField(label=_('Descriptive'), required=False, widget=forms.Textarea(attrs={'class':'giant asm'}))
    comments = forms.CharField(label=_('Comments'), required=False, widget=forms.Textarea(attrs={'class':'giant asm'}))
    class Meta:
        model = Session
        fields = ('occurrence', 'session_goals', 'descriptive', 'comments')
