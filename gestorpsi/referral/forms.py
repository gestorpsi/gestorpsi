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
from threadlocals.threadlocals import get_current_request

from gestorpsi.referral.models import Referral, ReferralPriority, ReferralImpact, ReferralDischarge, Queue, ReferralExternal
from gestorpsi.careprofessional.models import CareProfessional
from gestorpsi.client.models import Client 
from gestorpsi.service.models import Service, ServiceGroup
from gestorpsi.covenant.models import Covenant

'''
    Tiago de Souza Moraes / tiago@futuria.com.br
    update 06 10 2016
'''
class ReferralForm(forms.ModelForm):

    group = forms.ModelChoiceField(
            queryset=ServiceGroup.objects.all(),
            widget=forms.Select(attrs={'class':'extrabig asm', }),
            required=False
            )

    priority = forms.ModelChoiceField(
            queryset=ReferralPriority.objects.all(),
            widget=forms.Select(attrs={'class':'extramedium', }),
            required=False
            )

    impact = forms.ModelChoiceField(
            queryset=ReferralImpact.objects.all(),
            widget=forms.Select(attrs={'class':'giant', }),
            required=False
            )

    referral_reason = forms.CharField( 
            widget=forms.Textarea(attrs={'cols':'59','rows':'5' }),
            required=False
            )

    available_time = forms.CharField( 
            widget=forms.Textarea(attrs={'cols':'59','rows':'5'}),
            required=False
            )

    annotation = forms.CharField(
            widget=forms.Textarea(attrs={'cols':'59','rows':'5'}),
            required=False
            )

    class Meta:
        fields = ('service','professional', 'annotation', 'referral_reason', 'available_time', 'priority', 'impact', 'covenant')
        model = Referral
    
    def __init__(self, request, *args, **kwargs):
        '''
            request : Django session request
        '''
        super(ReferralForm, self).__init__(*args, **kwargs)

        if self.instance.id:
            wdgt = forms.Select(attrs={'class':'extrabig asm check_change','required':'required' })
        else:
            wdgt = forms.Select(attrs={'class':'extrabig asm','required':'required' })

        self.fields['service'] = forms.ModelChoiceField(
                    queryset=Service.objects.filter(active=True, organization=request.user.get_profile().org_active),
                    widget=wdgt,
                    required=True
                )

        """
            filter content of select based in service
            mount form or save
        """
        # professional
        # mount form / show professional of service
        if self.instance.id and self.instance.service and not request.POST:
            self.fields['professional'].queryset = CareProfessional.objects.filter(prof_services=self.instance.service, person__organization=request.user.get_profile().org_active)
        # new / update, allow all professional of org
        else:
            self.fields['professional'].queryset = CareProfessional.objects.filter(person__organization=request.user.get_profile().org_active)


        # groups of service
        if self.instance.id and self.instance.service.is_group and not request.POST:
            self.fields['group'].queryset = ServiceGroup.objects.filter(service=self.instance.service, service__organization=request.user.get_profile().org_active)

            if self.instance.group: # group is not required, can be None/Null
                self.fields['group'].initial = self.instance.group.id
        else:
            self.fields['group'].queryset = ServiceGroup.objects.filter(service__organization=request.user.get_profile().org_active)


        # covenant of service
        if self.instance.id and self.instance.service and not request.POST:
            self.fields['covenant'] = forms.ModelMultipleChoiceField(
                                        queryset=Covenant.objects.filter( organization=request.user.get_profile().org_active, active=True, service=self.instance.service),
                                        widget = forms.Select(attrs={'class':'check_change'}),
                                        required=False,
                                    )
        else:
            self.fields['covenant'] = forms.ModelMultipleChoiceField(
                                        queryset=Covenant.objects.filter( organization=request.user.get_profile().org_active, active=True ),
                                        required=False,
                                    )


class ReferralDischargeForm(forms.ModelForm):
    details = forms.CharField(label=_('Details'), widget=forms.Textarea(attrs={'class':'giant'}), required=False)
    description = forms.CharField(label=_('Description'), widget=forms.Textarea(attrs={'class':'giant'}), required=False)

    class Meta:
        fields = ('reason', 'was_discussed_with_client', 'details', 'status', 'description', )
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
        fields = ('comments','referral')
        model = ReferralExternal
