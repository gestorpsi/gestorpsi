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
from django.utils.translation import ugettext_lazy as _

from gestorpsi.organization.models import Organization
from gestorpsi.gcm.models import Invoice
from gestorpsi.gcm.models.plan import Plan

class InvoiceForm(forms.ModelForm):

    organization = forms.ModelChoiceField(label=(u'Organização'), queryset=Organization.objects.filter(organization=None).order_by('name'))
    plan = forms.ModelChoiceField(label=_('Plano'), queryset=Plan.objects.filter(active=True))

    class Meta:
        model = Invoice
