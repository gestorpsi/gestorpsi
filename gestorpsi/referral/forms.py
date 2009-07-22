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
from gestorpsi.referral.models import Referral, ReferralPriority, ReferralImpact, ReferralGroup
from gestorpsi.careprofessional.models import CareProfessional
from gestorpsi.client.models import Client
from gestorpsi.service.models import Service


class ReferralForm(forms.ModelForm):
    referral = forms.ModelChoiceField(queryset=Referral.objects.all(), required = False, widget=forms.Select(attrs={'class':'extrabig asm', }))
    service = forms.ModelChoiceField(queryset=Service.objects.all(), widget=forms.Select(attrs={'class':'extrabig asm', }))
    professional = forms.ModelMultipleChoiceField(queryset=CareProfessional.objects.all(), required = False, widget=forms.SelectMultiple(attrs={'class':'extrabig multiple asm', }))
    client = forms.ModelMultipleChoiceField(queryset=Client.objects.all(),  widget=forms.SelectMultiple(attrs={'class':'extrabig multiple asm', }))
    annotation = forms.CharField(widget=forms.Textarea(), required = False)
    referral_reason = forms.CharField(widget=forms.Textarea(), required = False)
    available_time = forms.CharField(widget=forms.Textarea(), required = False)
    priority = forms.ModelChoiceField(queryset=ReferralPriority.objects.all(), required = False, widget=forms.Select(attrs={'class':'extramedium', }))
    impact = forms.ModelChoiceField(queryset=ReferralImpact.objects.all(), required = False, widget=forms.Select(attrs={'class':'giant', }))
    
    
    class Meta:
        fields = ('client', 'service', 'professional', 'annotation', 'referral', 'annotation', 'referral_reason', 'available_time', 'priority', 'impact')
        model = Referral


class ReferralGroupForm(forms.ModelForm):
    description = forms.CharField(widget=forms.TextInput(attrs={'class':'giant', }))
    comments = forms.CharField(widget=forms.Textarea(attrs={'class':'giant', }), required = False)
    class Meta:
        fields = ('description', 'comments', )
        model = ReferralGroup

class ReferralClientForm(forms.ModelForm):
    client = forms.ModelMultipleChoiceField(queryset=Client.objects.all(),  widget=forms.SelectMultiple(attrs={'class':'giant high multiple multiselectable', }), required = False)
    class Meta:
        fields = ('client', )
        model = Referral
