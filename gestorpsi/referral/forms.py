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
from gestorpsi.referral.models import Referral,\
    ReferralPriority,\
    ReferralImpact, ReferralDischarge, Queue, ReferralExternal
from gestorpsi.careprofessional.models import CareProfessional
from gestorpsi.client.models import Client
from gestorpsi.service.models import Service, ServiceGroup


'''
    Tiago de Souza Moraes / tiago@futuria.com.br
    update 20 02 2014
'''


class ReferralForm(forms.ModelForm):

    referral = forms.ModelChoiceField(
        queryset=Referral.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'extrabig asm', }))
    service = forms.ModelChoiceField(
        queryset=Service.objects.all(),
        widget=forms.Select(attrs={'class': 'extrabig asm', }))
    group = forms.ModelChoiceField(
        queryset=ServiceGroup.objects.all(),
        required=False, widget=forms.Select(attrs={'class': 'extrabig asm', }))

    # professional = forms.MultipleChoiceField(required=False,
    # widget=forms.CheckboxSelectMultiple, choices = (
    # [(i.id, i) for i in CareProfessional.objects.all()]
    # ))

    client = forms.ModelMultipleChoiceField(
        queryset=Client.objects.all(),
        required=False,
        widget=forms.SelectMultiple(
            attrs={'class': 'extrabig multiple asm', }))
    annotation = forms.CharField(widget=forms.Textarea(), required=False)
    referral_reason = forms.CharField(
        widget=forms.Textarea(), required=False)
    available_time = forms.CharField(widget=forms.Textarea(), required=False)
    priority = forms.ModelChoiceField(
        queryset=ReferralPriority.objects.all(),
        required=False, widget=forms.Select(attrs={'class': 'extramedium', }))
    impact = forms.ModelChoiceField(queryset=ReferralImpact.objects.all(),
                                    required=False,
                                    widget=forms.Select(
                                        attrs={'class': 'giant', }))

    class Meta:
        fields = ('client', 'service', 'professional', 'annotation',
                  'referral', 'annotation', 'referral_reason',
                  'available_time', 'priority', 'impact')
        model = Referral

    def __init__(self, *args, **kwargs):
        super(ReferralForm, self).__init__(*args, **kwargs)
        if hasattr(self, 'instance') and self.instance.id:
            if self.instance.service.is_group:
            #if self.instance.service.is_group and self.instance.group:
                self.fields['group'].widget.attrs = {'class': 'extrabig asm',
                                                     'original_state': self.
                                                     instance.group.id}
                self.fields['group'].required = True


class ReferralDischargeForm(forms.ModelForm):
    details = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'giant'}), required=False)
    description = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'giant'}), required=False)

    class Meta:
        fields = ('reason', 'was_discussed_with_client', 'details', 'status',
                  'description', )
        model = ReferralDischarge

    def __init__(self, *args, **kwargs):
        super(ReferralDischargeForm, self).__init__(*args, **kwargs)
        self.initial.setdefault('referral', self.initial.get('referral', None))
        self.initial.setdefault('client', self.initial.get('client', None))


class QueueForm(forms.ModelForm):
    class Meta:
        fields = ('comments', 'client', 'referral')
        model = Queue


class ReferralExtForm(forms.ModelForm):
    class Meta:
        fields = ('comments', 'referral')
        model = ReferralExternal
