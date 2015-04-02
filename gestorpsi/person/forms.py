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
from gestorpsi.client.models import Client
from gestorpsi.person.models import Person, Company, CompanyClient


class CompanyForm(forms.ModelForm):
    cnae_class = forms.CharField(label=_('CNAE Class Code'),
                                 required=False,
                                 widget=forms.TextInput(
                                 attrs={'mask': '9999-9/99'}))

    class Meta:
        model = Company
        fields = ('size', 'cnae_class', )


class CompanyClientForm(forms.ModelForm):
    name = forms.CharField(required=True,
                           widget=forms.TextInput(attrs={'class': 'extrabig'}))

    class Meta:
        model = CompanyClient
        fields = ('name', 'responsible', 'active')

    def save(self, request, client, *args, **kwargs):
        company_client = super(CompanyClientForm, self).\
            save(commit=False, *args, **kwargs)
        company_client.company = client.person.company

        # client and person is new, lets create it before
        if not request.POST.get('client_id'):
            person = Person(name=request.POST.get('name'))
            person.save()
            person.organization.add(request.user.get_profile().org_active.id)
            client_related = Client(person=person,
                                    idRecord=request.user.get_profile().
                                    org_active.last_id_record + 1)
            client_related.save()
            company_client.active = True
        # client already exist, let's create or edit some existing relation
        else:
            # relation already exists, let's edit it
            if not request.POST.get('client_id') in [
                i.client.id for i in
                client.person.company.
                companyclient_set.all()]\
                    and not request.POST.get('active'):
                company_client.active = True
            client_related = Client.objects.get(pk=request.POST.get(
                'client_id'), person__organization=request.
                user.get_profile().org_active)

        company_client.client = client_related
        company_client.responsible = False if not request.POST.get(
            'responsible') else True
        company_client.save()

        return company_client
