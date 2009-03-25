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
from gestorpsi.referral.models import Referral
from gestorpsi.careprofessional.models import CareProfessional
from gestorpsi.client.models import Client
from gestorpsi.service.models import Service


class ReferralForm(forms.ModelForm):
    service = forms.ModelChoiceField(queryset=Service.objects.all(), widget=forms.Select(attrs={'class':'extrabig asm', }))
    professional = forms.ModelMultipleChoiceField(queryset=CareProfessional.objects.all(),  widget=forms.SelectMultiple(attrs={'class':'extrabig multiple asm', }))
    client = forms.ModelMultipleChoiceField(queryset=Client.objects.all(),  widget=forms.SelectMultiple(attrs={'class':'extrabig multiple asm', }))
    class Meta:
        fields = ('client', 'service', 'professional',)
        model = Referral

