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
from gestorpsi.authentication.forms import RegistrationForm
from gestorpsi.gcm.models import Plan, Invoice
from gestorpsi.phone.models import Phone
from gestorpsi.address.models import State, City, Address, AddressType
from gestorpsi.document.models import *
from gestorpsi.gcm.forms import fields

class RegistrationForm(RegistrationForm):
    plan = forms.ModelChoiceField(label=_('Access Plan'), help_text=_('Choice one access plan'), queryset=Plan.objects.filter(active=True))
    phone = forms.CharField(max_length=14, label=_('Phone Number'), help_text=_('Enter your phone number with area code here'), widget=forms.TextInput(attrs={'mask':'(99) 9999-9999?9',}))
    cpf = fields.CPFField(label=_('CPF Number'), help_text=_('Enter your CPF number here'), widget=forms.TextInput(attrs={'mask':'999.999.999-99',}))
    address = forms.CharField(max_length=255, label=_('Address Street'), help_text=_('Enter your address here'))
    address_number = forms.CharField(max_length=30, label=_('Address Number'), help_text=_('Enter your address number here'))
    zipcode = forms.CharField(max_length=30, label=_('ZIP Code'), help_text=_('Enter your ZIP Code here'))
    state = forms.ModelChoiceField(label=_('State/Region'), help_text=_('Enter your state/region here'), queryset=State.objects.all(), widget=forms.Select(attrs={'style':'width:265px;', 'class':'city_search'}))

    def save(self, request, *args, **kwargs):
        organization = super(RegistrationForm, self).save(False, *args, **kwargs) # send_email = False 
        i = Invoice()
        i.organization = organization
        i.plan = self.cleaned_data['plan']
        i.save()

        # add phone number to 'first' professional registered
        if self.cleaned_data['phone']:
            p = Phone()
            p.area = self.cleaned_data['phone'][1:3]
            p.phoneNumber = self.cleaned_data['phone'][5:14]
            p.phoneType_id = 2
            person = organization.care_professionals()[0]
            person.phones.add(p)
            
        # add cpf number to 'first' professional registered
        if self.cleaned_data['cpf']:
            d = Document()
            t = TypeDocument.objects.get(description='CPF')
            d.typeDocument_id = t.id
            d.document = self.cleaned_data['cpf']
            person.document.add(d)

        # add address to 'first' professional registered
        if self.cleaned_data['address']:
            a = Address()
            at = AddressType.objects.get(description='Comercial')
            a.addressType_id = at.id
            a.addressLine1 = self.cleaned_data['address']
            a.addressNumber = self.cleaned_data['address_number']
            a.zipCode = self.cleaned_data['zipcode']
            a.city_id = request.POST.get('city')
            person.address.add(a)
        
        
