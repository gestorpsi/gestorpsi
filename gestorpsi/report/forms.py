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
from django.utils.translation import gettext_lazy as _
from gestorpsi.report.models import Report, ReportsSaved, VIEWS_CHOICES
from gestorpsi.service.models import Service
from gestorpsi.financial.models import STATUS
from gestorpsi.careprofessional.models import CareProfessional
from datetime import datetime
from gestorpsi.schedule.models import OCCURRENCE_CONFIRMATION_PRESENCE

EXPORT_FORMATS = (
    (1, 'HTML'),
    (2, 'PDF'),
)

GRAPH_TYPE = (
    ('lines', 'Lines'),
    ('bars', 'Bars'),
    ('points', 'Points'),
)

GRAPH_ACCUMULATED = (
    (True, _('Accumulated Graph')),
    (False, _('Not accumulated Graph')),
)

class ReportForm(forms.ModelForm):
    """
    form used to filter results
    """
    view = forms.ChoiceField(choices=VIEWS_CHOICES)
    date_start = forms.CharField()
    date_end = forms.CharField()
    service = forms.ChoiceField(label=_('Service'))
    format = forms.ChoiceField(label=_('Export format'), choices=EXPORT_FORMATS, help_text=_('Here you can choose which format you want to export the data. For printing graphics please use HTML format'))
    clients = forms.BooleanField(label=_('Include client list'), help_text=_('If selected will a list of clients for each report sub-item'))
    accumulated = forms.ChoiceField(label=_('Accumulated Graph'), choices=GRAPH_ACCUMULATED, help_text=_('Acummulated graph?'))
    export_graph_type = forms.ChoiceField(label=_('Graph Type format'), choices=GRAPH_TYPE, help_text=_('Here you can choose which type of graph you need. Note: only for HTML format'))
    professional = forms.ModelChoiceField(label=_('Profissional'), queryset=CareProfessional.objects.all() )
    occurrence_status = forms.ChoiceField(label=_('Status do evento'), choices=OCCURRENCE_CONFIRMATION_PRESENCE, help_text=_('Status do evento'))
    
    class Meta:
        model = Report

    def __init__(self, date_start, date_end, organization, *args, **kwargs):
        super(ReportForm, self).__init__(*args, **kwargs)
        self.fields['view'].initial = 1 # admission view as default
        self.fields['accumulated'].initial = True # acummulated graph as default
        self.fields['date_start'].initial = date_start.strftime('%d/%m/%Y')
        self.fields['date_end'].initial = date_end.strftime('%d/%m/%Y')
        choices = [('',_('------ All Services ------'))]
        for i in Service.objects.filter(organization=organization, active=True):
            choices.append((i.pk, i.name))
        # services
        choices = [('',_('--- Todos ---'))]
        for i in Service.objects.filter(organization=organization, active=True):
            choices.append((i.pk, i.name))
        self.fields['service'].choices = choices

        # professional
        choices = [('all',_('--- Todos ---'))]
        for i in CareProfessional.objects.filter(person__organization=organization, active=True):
            choices.append((i.pk, i.person.name))
        self.fields['professional'].choices = choices

        # occurrence
        self.fields['occurrence_status'].choices = tuple([(u'all', '--- Todos ---')] + list(OCCURRENCE_CONFIRMATION_PRESENCE))


class ReportSaveForm(forms.ModelForm):
    """
    form used to save json result into database
    'save reports' function
    """

    class Meta:
        model = ReportsSaved
        fields = ('label', 'data', )

    def __init__(self, *args, **kwargs):
        super(ReportSaveForm, self).__init__(*args, **kwargs)
        self.fields['data'].widget = forms.HiddenInput()
        self.fields['label'].widget.attrs = {'class':'mini_form_input'}

class ReportSaveAdmissionForm(ReportSaveForm):
    """
    admission form save report view
    'save reports' function
    """
    def __init__(self, *args, **kwargs):
        date_start = kwargs.pop('date_start', None)
        date_end = kwargs.pop('date_end', None)
        service = kwargs.pop('service', None)
        accumulated = kwargs.pop('accumulated', None)
        super(ReportSaveAdmissionForm, self).__init__(*args, **kwargs)
        if date_start and date_end:
            self.fields['label'].initial = '%s %s %s %s' % (_('Admission between'), date_start.strftime("%d/%m/%Y"),  _('and'), date_end.strftime("%d/%m/%Y"))
            self.fields['data'].initial = 'view=admission&date_start=%s&date_end=%s&accumulated=%s'% (date_start.strftime("%d/%m/%Y"), date_end.strftime("%d/%m/%Y"), accumulated)

    def save(self, user, organization, *args, **kwargs):
        data = super(ReportSaveAdmissionForm, self).save(commit=False, *args, **kwargs)
        data.view = 1 # admission
        data.user = user
        data.organization = organization
        data.save()
        return data

class ReportSaveReferralForm(ReportSaveForm):
    """
    admission form save report view
    'save reports' function
    """
    def __init__(self, *args, **kwargs):
        date_start = kwargs.pop('date_start', None)
        date_end = kwargs.pop('date_end', None)
        service = kwargs.pop('service', None)
        accumulated = kwargs.pop('accumulated', None)
        super(ReportSaveReferralForm, self).__init__(*args, **kwargs)
        if date_start and date_end:
            self.fields['label'].initial = u'%s%s %s %s %s' % ('' if not service else (u'%s - ' % service), _('Referrals between'), date_start.strftime("%d/%m/%Y"),  _('and'), date_end.strftime("%d/%m/%Y"))
            self.fields['data'].initial = 'view=referral&date_start=%s&date_end=%s&service=%s&accumulated=%s'% (date_start.strftime("%d/%m/%Y"), date_end.strftime("%d/%m/%Y"), '' if not service else service.pk, accumulated)

    def save(self, user, organization, *args, **kwargs):
        data = super(ReportSaveReferralForm, self).save(commit=False, *args, **kwargs)
        data.view = 2 # referral
        data.user = user
        data.organization = organization
        data.save()
        return data


