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
from gestorpsi.client.models import Family
from gestorpsi.person.models import Person
from gestorpsi.client.models import Client


class FamilyForm(forms.ModelForm):
    name = forms.CharField(required=True,
                           widget=forms.TextInput(attrs={'class': 'big'}))

    class Meta:
        model = Family
        fields = ('name', 'relation_level', 'responsible', 'active', 'comment')

    def save(self, request, client, *args, **kwargs):
        family = super(FamilyForm, self).save(*args, **kwargs)
        family.client = client
        if request.POST.get('client_id'):  # existing client
            client_related = Client.objects.filter(
                pk=request.POST.get('client_id'),
                person__organization=request.user.get_profile().org_active)[0]
        else:  # client and person is new, lets create it before
            person = Person(name=request.POST.get('name'))
            person.save()
            person.organization.add(request.user.get_profile().org_active.id)
            client_related = Client(person=person,
                                    idRecord=request.user.get_profile().
                                    org_active.last_id_record + 1)
            client_related.save()

        family.client_related = client_related
        family.save()
        return family
