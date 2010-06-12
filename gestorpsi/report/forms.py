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
from datetime import datetime

EXPORT_FORMATS = (
    (1, 'HTML'),
    (2, 'PDF'),
)

class ReportForm(forms.ModelForm):
    """
    form used to filter results
    """
    view = forms.ChoiceField(choices=VIEWS_CHOICES)
    date_start = forms.CharField()
    date_end = forms.CharField()
    format = forms.ChoiceField(label=_('Export format'), choices=EXPORT_FORMATS, help_text=_('Here you can choose which format you want to export the data. For printing graphics please use HTML format'))
    clients = forms.BooleanField(label=_('Include client list'), help_text=_('If selected will a list of clients for each report sub-item'))

    class Meta:
        model = Report

    def __init__(self, date_start, date_end, *args, **kwargs):
        super(ReportForm, self).__init__(*args, **kwargs)
        self.fields['view'].initial = 1 # admission view as default
        self.fields['date_start'].initial = date_start.strftime('%d/%m/%Y')
        self.fields['date_end'].initial = date_end.strftime('%d/%m/%Y')

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
        super(ReportSaveAdmissionForm, self).__init__(*args, **kwargs)
        if date_start and date_end:
            self.fields['label'].initial = _('Admission between %s and %s' % (date_start.strftime("%d/%m/%Y"), date_end.strftime("%d/%m/%Y")))
            self.fields['data'].initial = 'view=admission&date_start=%s&date_end=%s'% (date_start.strftime("%d/%m/%Y"), date_end.strftime("%d/%m/%Y"))

    def save(self, user, organization, *args, **kwargs):
        data = super(ReportSaveAdmissionForm, self).save(commit=False, *args, **kwargs)
        data.view = 1 # admission
        data.user = user
        data.organization = organization
        data.save()
        return data


